import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import face_recognition
import os
import sys

class FaceApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Face Password System")
        self.window.geometry("800x650")
        self.window.configure(bg="#f0f0f0")
        
        # State variables
        self.process_this_frame = True
        self.face_locations = []
        self.face_names = []
        self.known_encoding = None
        
        # 1. SETUP STORAGE
        # Use relative path to find the image
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(base_dir, "folder-path", "person.jpg")
        
        self.known_encoding = self.load_authorized_face()

        # 2. INITIALIZE CAMERA
        self.cap = cv2.VideoCapture(0)
        
        # 3. GUI SETUP
        self.setup_ui()
        
        # 4. PROTOCOLS
        self.window.protocol("WM_DELETE_WINDOW", self.exit_app)

        # Start the loop
        self.update_frame()

    def setup_ui(self):
        # Header
        header = tk.Label(self.window, text="Secure Face Scanner", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        header.pack(pady=10)

        # Video Frame
        self.video_container = tk.Frame(self.window, bg="black", bd=2, relief="sunken")
        self.video_container.pack(expand=True, fill="both", padx=20, pady=10)
        
        self.video_label = tk.Label(self.video_container, bg="black")
        self.video_label.pack(expand=True)

        # Status Label
        self.status_var = tk.StringVar(value="Waiting for scan...")
        self.status_label = tk.Label(self.window, textvariable=self.status_var, font=("Arial", 16), bg="#f0f0f0")
        self.status_label.pack(pady=10)

        # Exit Button
        self.btn_exit = tk.Button(self.window, text="Exit Application", command=self.exit_app, 
                                 bg="#d32f2f", fg="white", font=("Arial", 12, "bold"), width= 20)
        self.btn_exit.pack(pady=20)

    def load_authorized_face(self):
        """Helper to load and encode the reference image."""
        if os.path.exists(self.image_path):
            try:
                img = face_recognition.load_image_file(self.image_path)
                encodings = face_recognition.face_encodings(img)
                if encodings:
                    print("✅ Authorized face loaded successfully!")
                    return encodings[0]
                else:
                    print("❌ Error: No face found in person.jpg")
                    messagebox.showerror("Error", "No face found in reference image 'person.jpg'.")
                    return None
            except Exception as e:
                print(f"❌ Error loading image: {e}")
                return None
        else:
            print(f"❌ Error: Cannot find {self.image_path}")
            messagebox.showwarning("Configuration Error", f"File not found:\n{self.image_path}\n\nPlease place 'person.jpg' in 'folder-path'.")
            return None

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Only process every other frame of video to save time
            if self.process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                
                # Only encode if we have an authorized face to compare against
                if self.known_encoding is not None:
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
                    self.face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces([self.known_encoding], face_encoding, tolerance=0.5)
                        name = "Unknown"

                        if True in matches:
                            name = "Authorized"

                        self.face_names.append(name)
                else:
                    # If no reference face is loaded, everyone is unknown (or just mark as System Error)
                    self.face_names = ["No Reference"] * len(self.face_locations)

            self.process_this_frame = not self.process_this_frame

            # Display the results
            access_granted = False
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Choose color
                if name == "Authorized":
                    color = (0, 255, 0) # Green
                    access_granted = True
                else:
                    color = (0, 0, 255) # Red

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Update Status Label
            if access_granted:
                self.status_var.set("✅ ACCESS GRANTED")
                self.status_label.config(fg="green")
            elif self.face_names:
                self.status_var.set("⛔ UNAUTHORIZED")
                self.status_label.config(fg="red")
            else:
                self.status_var.set("Scanning...")
                self.status_label.config(fg="#555")

            # --- DISPLAY IN TKINTER ---
            cv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv_img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        
        # Schedule the next update
        self.window.after(10, self.update_frame)

    def exit_app(self):
        print("Shutting down...")
        if self.cap.isOpened():
            self.cap.release()
        self.window.destroy()
        sys.exit()

# --- RUNNING THE PROGRAM ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceApp(root)
    root.mainloop()