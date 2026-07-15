from plyer import notification
from src.config.settings import config_manager
from src.utils.logger import app_logger

class Notifier:
    @staticmethod
    def send_alert(student_id: str, behavior: str, time_str: str):
        if not config_manager.config.notifications_enabled:
            return
        
        title = "Cheating Detected!"
        message = f"Student ID: {student_id}\nBehavior: {behavior}\nTime: {time_str}\nScreenshot Saved."
        
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Cheating Alert System",
                timeout=5
            )
        except Exception as e:
            app_logger.error(f"Notification failed: {e}")