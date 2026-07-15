import numpy as np
from ultralytics import YOLO
from src.config.settings import config_manager
from src.utils.logger import app_logger


class AIEngine:
    def __init__(self):
        try:
            self.model = YOLO(config_manager.config.model_path)
            self.model.to("cpu")
            app_logger.info("YOLO model loaded successfully.")
        except Exception as e:
            app_logger.error(f"Failed to load YOLO model: {e}")
            self.model = None

    def process_frame(self, frame: np.ndarray) -> list:
        if self.model is None:
            return []
        try:
            results = self.model.track(
                frame,
                verbose=False,
                conf=config_manager.config.confidence_threshold,
                iou=config_manager.config.iou_threshold,
                persist=True,
                tracker="bytetrack.yaml",
            )
            detections = []
            if results and results[0].boxes is not None:
                boxes = results[0].boxes
                if boxes.id is None:
                    return detections
                for box, track_id in zip(boxes, boxes.id):
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    class_id = int(box.cls[0])
                    detections.append({
                        "id": int(track_id),
                        "bbox": (x1, y1, x2, y2),
                        "confidence": conf,
                        "class_id": class_id
                    })
            return detections
        except Exception as e:
            app_logger.error(f"Error processing frame: {e}")
            return []

    def reset(self):
        if self.model is not None:
            self.model.predictor = None
