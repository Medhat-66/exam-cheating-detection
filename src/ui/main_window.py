import customtkinter as ctk
from PIL import Image
import cv2
import numpy as np

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Cheating Tracking and Alert System")
        self.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="AI Alert System", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.upload_btn = ctk.CTkButton(self.sidebar_frame, text="Upload Video", height=40)
        self.upload_btn.grid(row=1, column=0, padx=20, pady=10)

        self.start_btn = ctk.CTkButton(self.sidebar_frame, text="Start Detection", fg_color="#28a745", hover_color="#218838", height=40)
        self.start_btn.grid(row=2, column=0, padx=20, pady=10)

        self.stop_btn = ctk.CTkButton(self.sidebar_frame, text="Stop Detection", fg_color="#dc3545", hover_color="#c82333", height=40)
        self.stop_btn.grid(row=3, column=0, padx=20, pady=10)

        self.settings_btn = ctk.CTkButton(self.sidebar_frame, text="Settings", height=40)
        self.settings_btn.grid(row=4, column=0, padx=20, pady=10)

        self.stats_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Alerts Today: 0\nAvg Confidence: 0%", 
            font=ctk.CTkFont(size=14)
        )
        self.stats_label.grid(row=5, column=0, padx=20, pady=20)

        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.video_label = ctk.CTkLabel(self.main_frame, text="No Video Loaded", font=ctk.CTkFont(size=20))
        self.video_label.grid(row=0, column=0, sticky="nsew")

    def update_video_frame(self, frame: np.ndarray):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        img = Image.fromarray(frame_rgb)
        
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(850, 650))
        
        self.video_label.configure(image=ctk_img, text="")
        self.video_label.image = ctk_img

    def update_statistics(self, alerts_count: int, avg_conf: float):
        self.stats_label.configure(text=f"Alerts Today: {alerts_count}\nAvg Confidence: {avg_conf}%")