"""
Face Password System - Android/Kivy Version
Converts the original tkinter app to work on Android devices
"""
import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import face_recognition
import os
from PIL import Image as PILImage
import threading

class FacePasswordApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.known_encoding = None
        self.camera_widget = None
        self.status_label = None
        self.capture_thread = None
        self.is_running = True
        
    def build(self):
        """Build the UI layout"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Top label for status
        self.status_label = Label(
            text="Waiting for scan...",
            size_hint_y=0.15,
            font_size='20sp',
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Camera widget
        self.camera_widget = Camera(
            resolution=(640, 480),
            size_hint_y=0.7
        )
        main_layout.add_widget(self.camera_widget)
        
        # Bottom buttons layout
        button_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        btn_capture = Button(text="Scan Face", background_color=(0.2, 0.6, 1, 1))
        btn_capture.bind(on_press=self.start_face_scan)
        button_layout.add_widget(btn_capture)
        
        btn_exit = Button(text="Exit", background_color=(1, 0.2, 0.2, 1))
        btn_exit.bind(on_press=self.exit_app)
        button_layout.add_widget(btn_exit)
        
        main_layout.add_widget(button_layout)
        
        # Load authorized face
        self.load_authorized_face()
        
        # Start frame update loop
        Clock.schedule_interval(self.update_frame, 0.033)  # ~30 FPS
        
        return main_layout
    
    def load_authorized_face(self):
        """Load and encode the reference face"""
        store_path = self.get_storage_path()
        image_path = os.path.join(store_path, "person.jpg")
        
        if os.path.exists(image_path):
            try:
                img = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(img)
                if encodings:
                    self.known_encoding = encodings[0]
                    self.update_status("✓ Authorized face loaded", "green")
                    print("✅ Authorized face loaded successfully!")
                else:
                    self.update_status("✗ No face in reference image", "red")
                    print("❌ Error: No face found in reference image")
            except Exception as e:
                self.update_status(f"✗ Error loading face: {str(e)}", "red")
                print(f"❌ Error: {e}")
        else:
            self.update_status(f"✗ Reference image not found", "red")
            print(f"❌ Error: Cannot find {image_path}")
    
    def start_face_scan(self, instance):
        """Start scanning for face match"""
        if self.camera_widget:
            self.update_status("Scanning...", "yellow")
            Clock.schedule_once(self.perform_face_scan, 0.5)
    
    def perform_face_scan(self, dt):
        """Perform the actual face recognition"""
        if self.camera_widget and self.camera_widget.texture:
            try:
                # Capture frame from camera
                texture = self.camera_widget.texture
                frame = self.texture_to_cv2(texture)
                
                if frame is not None and self.known_encoding is not None:
                    # Resize for faster processing
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                    
                    # Find faces
                    face_locs = face_recognition.face_locations(rgb_small)
                    face_encs = face_recognition.face_encodings(rgb_small, face_locs)
                    
                    if face_encs:
                        for face_encoding in face_encs:
                            matches = face_recognition.compare_faces(
                                [self.known_encoding], 
                                face_encoding, 
                                tolerance=0.6
                            )
                            
                            if True in matches:
                                self.update_status("✓ ACCESS GRANTED", "green")
                                print("✅ SCANNER: Match Found!")
                            else:
                                self.update_status("✗ UNKNOWN USER", "red")
                                print("❌ SCANNER: Unauthorized Face")
                    else:
                        self.update_status("No face detected", "yellow")
            except Exception as e:
                self.update_status(f"Error: {str(e)}", "red")
                print(f"❌ Scan error: {e}")
    
    def update_frame(self, dt):
        """Update camera frame continuously"""
        # Camera widget handles display automatically
        pass
    
    def texture_to_cv2(self, texture):
        """Convert Kivy texture to OpenCV format"""
        try:
            buf = texture.pixels
            img_data = np.frombuffer(buf, np.uint8)
            img_data = img_data.reshape(texture.height, texture.width, 4)
            # Convert RGBA to BGR for OpenCV
            frame = cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)
            return frame
        except Exception as e:
            print(f"Error converting texture: {e}")
            return None
    
    def update_status(self, message, color="white"):
        """Update status label"""
        color_map = {
            "green": (0, 1, 0, 1),
            "red": (1, 0, 0, 1),
            "yellow": (1, 1, 0, 1),
            "white": (1, 1, 1, 1)
        }
        self.status_label.text = message
        self.status_label.color = color_map.get(color, (1, 1, 1, 1))
    
    def get_storage_path(self):
        """Get appropriate storage path for Android/Desktop"""
        try:
            # Try to get Android app storage path (only available when running on Android)
            import android  # noqa: F401
            from android.app import PythonActivity  # noqa: F401
            app_path = PythonActivity.mActivity.getFilesDir().toString()
            return app_path
        except (ImportError, AttributeError, NameError):
            # Desktop fallback
            return r"I:\Coding\python\face-password\folder-path"
    
    def exit_app(self, instance):
        """Exit the application"""
        print("Shutting down...")
        self.is_running = False
        App.get_running_app().stop()

if __name__ == "__main__":
    FacePasswordApp().run()
