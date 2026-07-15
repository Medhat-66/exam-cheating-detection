import cv2
import os
from datetime import datetime
from src.config.settings import config_manager
from src.utils.logger import app_logger

class ScreenshotManager:
    @staticmethod
    def save_screenshot(frame, student_id: str, behavior: str) -> str:
        if not config_manager.config.save_screenshots:
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_behavior = behavior.replace(" ", "_").lower()
        filename = f"student_{student_id}_{safe_behavior}_{timestamp}.jpg"
        filepath = os.path.join(config_manager.config.screenshot_dir, filename)
        
        try:
            cv2.imwrite(filepath, frame)
            return filepath
        except Exception as e:
            app_logger.error(f"Screenshot save failed: {e}")
            return ""