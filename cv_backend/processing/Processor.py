import math
from queue import Queue
from threading import Thread
from FcmManager import FcmManager
from Firestore import Firestore
import time

classNames = ["Lie", "Sit", "Stand", ""]
# box = {{x1, y1}, {x2, y2}, cls}

class Processor(object):
    def __init__(self, duration=1):
        self.q = Queue()
        self.duration = duration
        self.prev = 3
        self.fcmManager = FcmManager()
        self.firestore = Firestore()
        self.prev = set()
        
        self.thread = Thread(target=self.process, args=())
        self.thread.daemon = True
        self.thread.start()


    def _get_dist(self, box1, box2):
        # get the euclidean dist between lt points
        return math.sqrt((box1[0][0] - box2[0][0])**2 + (box1[0][1] - box2[0][1])**2)
    
    def _group_similar_points(self, boxes: list[tuple[tuple[float, float], tuple[float, float], str]], threshold = 0.07):
        groups: list[list[tuple[tuple[float, float], tuple[float, float], str]]] = []
        
        for box in boxes:
            added_to_group = False
            for group in groups:
                group_type = group[0][2]
                if box[2] == group_type and any(self._get_dist(box, group_point) <= threshold for group_point in group):
                    group.append(box)
                    added_to_group = True
                    break
        
            if not added_to_group:
                groups.append([box])
        return groups
    
    def _get_center(self, point: tuple[tuple[float, float], tuple[float, float], str]) -> tuple[float, float, str]:
        return ((point[0][0]+point[1][0])/2, (point[0][1]+point[0][1])/2, point[2])

    def _check_trigger(self, center_point: tuple[float, float, int]) -> list[str]:
        ret = []
        res: set[str] = set()
        triggers = self.firestore.db.collection(u'trigger').stream()

        for trigger_raw_json in triggers:
            trigger_raw: dict[str, dict[str, str]] = trigger_raw_json.to_dict()
            trigger_key = list(trigger_raw.keys())[0]
            trigger: dict[str, str] = trigger_raw[trigger_key]

            if trigger['detectPosture'] == center_point[2] and float(trigger['lt_x']) <= center_point[0] <= float(trigger['rb_x']) and float(trigger['lt_y']) <= center_point[1] <= float(trigger['rb_y']):
                print("detected", center_point, center_point[2])
                if not (trigger['routineId'] in self.prev):
                    ret.append(trigger['routineId'])
                res.add(trigger['routineId'])
        
        self.prev = res

        return ret        

    def process(self):
        while True:
            boxes: list[tuple[tuple[float, float], tuple[float, float], str]]=list(self.q.queue)
            self.q = Queue()

            groups = self._group_similar_points(boxes)
            
            for group in groups:
                if len(group) > 10:
                    target = sorted(group)[len(group)//2]
                    target_center = self._get_center(target)
                    
                    routine_ids = self._check_trigger(target_center)

                    for routine_id in routine_ids:
                        self.fcmManager.send_fcm_message(routine_id)
        
            time.sleep(self.duration)

    def push(self, object):
        self.q.put(object)
        
        
    
