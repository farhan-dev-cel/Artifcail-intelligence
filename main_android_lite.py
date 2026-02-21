"""
Face Password System - Android/Kivy Version (Simplified)
Optimized for Android with minimal dependencies
"""
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.garden.xcamera import XCamera
import os

class FacePasswordApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera_widget = None
        self.status_label = None
        self.is_running = True
        self.reference_image = None
        
    def build(self):
        """Build the UI layout"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Top label for status
        self.status_label = Label(
            text="Face Password System\nWaiting for scan...",
            size_hint_y=0.15,
            font_size='18sp',
            color=(0.2, 0.8, 0.2, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Camera widget - using built-in Camera
        self.camera_widget = Camera(
            resolution=(640, 480),
            size_hint_y=0.7,
            play=True
        )
        main_layout.add_widget(self.camera_widget)
        
        # Bottom buttons layout
        button_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        btn_capture = Button(
            text="Capture\nReference",
            background_color=(0.2, 0.6, 1, 1),
            font_size='14sp'
        )
        btn_capture.bind(on_press=self.capture_reference_face)
        button_layout.add_widget(btn_capture)
        
        btn_scan = Button(
            text="Scan Face",
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='14sp'
        )
        btn_scan.bind(on_press=self.start_face_scan)
        button_layout.add_widget(btn_scan)
        
        btn_exit = Button(
            text="Exit",
            background_color=(1, 0.2, 0.2, 1),
            font_size='14sp'
        )
        btn_exit.bind(on_press=self.exit_app)
        button_layout.add_widget(btn_exit)
        
        main_layout.add_widget(button_layout)
        
        # Load existing reference if available
        self.load_reference_image()
        
        return main_layout
    
    def capture_reference_face(self, instance):
        """Capture and save reference face"""
        self.update_status("Capturing reference face...", "yellow")
        Clock.schedule_once(self.save_reference_face, 1.0)
    
    def save_reference_face(self, dt):
        """Save the current camera frame as reference"""
        try:
            if self.camera_widget and self.camera_widget.texture:
                # Get filename with timestamp
                store_path = self.get_storage_path()
                os.makedirs(store_path, exist_ok=True)
                image_path = os.path.join(store_path, "person.jpg")
                
                # Save the current texture as reference
                self.camera_widget.export_to_png(image_path)
                
                self.update_status("✓ Reference face saved!", "green")
                print(f"✅ Reference face saved to {image_path}")
        except Exception as e:
            self.update_status(f"✗ Error saving: {str(e)}", "red")
            print(f"❌ Error saving reference: {e}")
    
    def load_reference_image(self):
        """Load reference image if it exists"""
        try:
            store_path = self.get_storage_path()
            image_path = os.path.join(store_path, "person.jpg")
            
            if os.path.exists(image_path):
                self.reference_image = image_path
                self.update_status("✓ Reference image loaded\nClick 'Scan Face' to verify", "green")
                print("✅ Reference image loaded successfully!")
            else:
                self.update_status("No reference image\nClick 'Capture Reference' first", "yellow")
                print("⚠️ No reference image found. Capture one first.")
        except Exception as e:
            self.update_status(f"✗ Error loading: {str(e)}", "red")
            print(f"❌ Error: {e}")
    
    def start_face_scan(self, instance):
        """Start scanning for face match"""
        if self.reference_image:
            self.update_status("Scanning...", "yellow")
            Clock.schedule_once(self.perform_face_scan, 0.5)
        else:
            self.update_status("No reference face!\nCapture one first", "red")
    
    def perform_face_scan(self, dt):
        """Perform the actual face scan"""
        try:
            import cv2
            import face_recognition
            
            if self.camera_widget and self.camera_widget.texture:
                # Capture frame from camera
                frame = self.texture_to_cv2(self.camera_widget.texture)
                
                if frame is not None and self.reference_image:
                    try:
                        # Load reference image
                        ref_img = face_recognition.load_image_file(self.reference_image)
                        ref_encodings = face_recognition.face_encodings(ref_img)
                        
                        if not ref_encodings:
                            self.update_status("No face in reference image", "red")
                            return
                        
                        known_encoding = ref_encodings[0]
                        
                        # Resize current frame for faster processing
                        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                        
                        # Find faces in current frame
                        face_locs = face_recognition.face_locations(rgb_small)
                        face_encs = face_recognition.face_encodings(rgb_small, face_locs)
                        
                        if face_encs:
                            match_found = False
                            for face_encoding in face_encs:
                                matches = face_recognition.compare_faces(
                                    [known_encoding], 
                                    face_encoding, 
                                    tolerance=0.6
                                )
                                
                                if True in matches:
                                    self.update_status("✓ ACCESS GRANTED!", "green")
                                    print("✅ MATCH FOUND!")
                                    match_found = True
                                    break
                            
                            if not match_found:
                                self.update_status("✗ UNKNOWN USER", "red")
                                print("❌ No match found")
                        else:
                            self.update_status("No face detected in scan", "yellow")
                    except IndexError:
                        self.update_status("✗ No face detected", "red")
                    except Exception as e:
                        self.update_status(f"✗ Error: {str(e)}", "red")
                        print(f"❌ Scan error: {e}")
        except ImportError as e:
            self.update_status(f"✗ Missing: {str(e)}", "red")
            print(f"❌ Import error: {e}")
    
    def texture_to_cv2(self, texture):
        """Convert Kivy texture to OpenCV format"""
        try:
            import cv2
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
            "green": (0.2, 1, 0.2, 1),
            "red": (1, 0.2, 0.2, 1),
            "yellow": (1, 1, 0.2, 1),
            "white": (1, 1, 1, 1)
        }
        self.status_label.text = message
        self.status_label.color = color_map.get(color, (1, 1, 1, 1))
    
    def get_storage_path(self):
        """Get appropriate storage path for Android/Desktop"""
        try:
            # Try to get Android app storage path
            from android.app import PythonActivity
            app_path = PythonActivity.mActivity.getFilesDir().toString()
            return app_path
        except (ImportError, AttributeError):
            # Desktop fallback
            return r"I:\Coding\python\face-password\folder-path"
    
    def exit_app(self, instance):
        """Exit the application"""
        print("Shutting down...")
        self.is_running = False
        App.get_running_app().stop()

if __name__ == "__main__":
    FacePasswordApp().run()
