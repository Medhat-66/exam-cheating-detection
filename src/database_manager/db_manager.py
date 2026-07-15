import sqlite3
from datetime import datetime
from src.config.settings import config_manager
from src.utils.logger import app_logger

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.db_path = config_manager.config.database_path
            cls._instance._create_tables()
        return cls._instance

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cheating_alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id TEXT NOT NULL,
                        behavior TEXT NOT NULL,
                        confidence REAL,
                        time TEXT,
                        date TEXT,
                        screenshot_path TEXT,
                        video_name TEXT,
                        alert_status TEXT DEFAULT 'Unread'
                    )
                ''')
                conn.commit()
        except Exception as e:
            app_logger.error(f"Database creation error: {e}")

    def insert_alert(self, student_id: str, behavior: str, confidence: float, screenshot_path: str, video_name: str):
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO cheating_alerts 
                    (student_id, behavior, confidence, time, date, screenshot_path, video_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (student_id, behavior, confidence, time_str, date_str, screenshot_path, video_name))
                conn.commit()
        except Exception as e:
            app_logger.error(f"Failed to insert alert: {e}")

    def get_all_alerts(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM cheating_alerts ORDER BY id DESC")
                return cursor.fetchall()
        except Exception as e:
            app_logger.error(f"Failed to fetch alerts: {e}")
            return []

    def get_statistics(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM cheating_alerts")
                total_cheating = cursor.fetchone()[0]
                
                today_str = datetime.now().strftime("%Y-%m-%d")
                cursor.execute("SELECT COUNT(*) FROM cheating_alerts WHERE date = ?", (today_str,))
                alerts_today = cursor.fetchone()[0]
                
                cursor.execute("SELECT AVG(confidence) FROM cheating_alerts")
                avg_conf = cursor.fetchone()[0]
                avg_confidence = round(avg_conf, 2) if avg_conf else 0.0
                
                return {
                    "total_cheating": total_cheating,
                    "alerts_today": alerts_today,
                    "avg_confidence": avg_confidence
                }
        except Exception as e:
            app_logger.error(f"Failed to fetch statistics: {e}")
            return {"total_cheating": 0, "alerts_today": 0, "avg_confidence": 0.0}

db_manager = DatabaseManager()