import math

class BehaviorAnalyzer:
    def __init__(self, history_length: int = 10):
        pass

    def _calculate_centroid(self, bbox: tuple) -> tuple:
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def analyze(self, detections: list) -> list:
        analyzed_detections = []
        students = [d for d in detections if d.get("class_id") == 0]
        others = [d for d in detections if d.get("class_id") != 0]

        for s in students:
            s_behavior = "Normal"
            sx1, sy1, sx2, sy2 = s["bbox"]
            
            s_bottom_y_threshold = sy2 - ((sy2 - sy1) * 0.4)
            
            for obj in others:
                ox1, oy1, ox2, oy2 = obj["bbox"]
                o_center_x = (ox1 + ox2) / 2
                o_center_y = (oy1 + oy2) / 2
                
                is_inside_x = sx1 < o_center_x < sx2
                is_inside_y = sy1 < o_center_y < sy2
                is_in_hand_zone = o_center_y > s_bottom_y_threshold
                
                if is_inside_x and is_inside_y and is_in_hand_zone:
                    s_behavior = "Cheating (Phone Detected)"
                    break
            
            s["behavior"] = s_behavior
            analyzed_detections.append(s)
            
        return analyzed_detections