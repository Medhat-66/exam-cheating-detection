import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import cv2
import threading
import queue
import time
import traceback
from tkinter import filedialog
import customtkinter as ctk

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.settings import config_manager
from src.utils.logger import app_logger
from src.database_manager.db_manager import db_manager
from src.notification.notifier import Notifier
from src.utils.screenshot import ScreenshotManager
from src.core.engine import AIEngine
from src.behavior.analyzer import BehaviorAnalyzer
from src.ui.main_window import MainWindow


class AppController:
    def __init__(self):
        self.app = MainWindow()
        self.ai_engine = AIEngine()
        self.behavior_analyzer = BehaviorAnalyzer()
        self.video_path = None
        self.is_running = False
        self.alerted_students = set()
        self.frame_queue = queue.Queue(maxsize=2)
        self._setup_connections()
        self._update_stats_ui()
        self.app.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._poll_frame_queue()

    def _setup_connections(self):
        self.app.upload_btn.configure(command=lambda: self.upload_video())
        self.app.start_btn.configure(command=lambda: self.start_processing())
        self.app.stop_btn.configure(command=lambda: self.stop_processing())

    def _update_stats_ui(self):
        stats = db_manager.get_statistics()
        self.app.update_statistics(stats["alerts_today"], stats["avg_confidence"])

    def upload_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
        if path:
            self.video_path = path
            self.app.video_label.configure(text=f"Loaded: {path.split('/')[-1]}")

    def start_processing(self):
        if self.is_running:
            return
        self.is_running = True
        self.alerted_students.clear()
        self.ai_engine.reset()
        threading.Thread(target=self._process_video_thread, daemon=True).start()

    def stop_processing(self):
        self.is_running = False
        self.video_path = None
        self.app.video_label.configure(text="No Video Loaded")

    def _open_capture(self):
        if self.video_path is not None:
            return cv2.VideoCapture(self.video_path)

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap

        cap.release()
        return cv2.VideoCapture(0)

    def _process_video_thread(self):
        try:
            cap = self._open_capture()

            if not cap.isOpened():
                app_logger.error("Could not open camera or video file.")
                self.is_running = False
                return

            while self.is_running:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.resize(frame, (640, 480))
                detections = self.ai_engine.process_frame(frame)
                analyzed_detections = self.behavior_analyzer.analyze(detections)

                for det in analyzed_detections:
                    x1, y1, x2, y2 = det["bbox"]
                    student_id = det.get("id", "Unknown")

                    if det["behavior"] != "Normal":
                        if student_id not in self.alerted_students:
                            self._trigger_alert(frame, student_id, det["behavior"], det["confidence"])
                            self.alerted_students.add(student_id)
                    else:
                        if student_id in self.alerted_students:
                            self.alerted_students.remove(student_id)

                    color = (0, 0, 255) if det["behavior"] != "Normal" else (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                if not self.frame_queue.full():
                    self.frame_queue.put(frame)

            cap.release()
            self.is_running = False
        except Exception:
            traceback.print_exc()
            self.is_running = False

    def _poll_frame_queue(self):
        try:
            while not self.frame_queue.empty():
                frame = self.frame_queue.get_nowait()
                self.app.update_video_frame(frame)
        except queue.Empty:
            pass
        self.app.after(30, self._poll_frame_queue)

    def _trigger_alert(self, frame, student_id, behavior, conf):
        screenshot_path = ScreenshotManager.save_screenshot(frame, str(student_id), behavior)
        db_manager.insert_alert(str(student_id), behavior, conf, screenshot_path, "video")
        Notifier.send_alert(str(student_id), behavior, time.strftime("%H:%M:%S"))
        self.app.after(0, self._update_stats_ui)

    def _on_closing(self):
        self.is_running = False
        self.app.destroy()


if __name__ == "__main__":
    controller = AppController()
    controller.app.mainloop()
