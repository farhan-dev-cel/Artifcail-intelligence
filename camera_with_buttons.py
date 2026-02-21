import cv2
import tkinter as tk
from tkinter import messagebox
import threading

class CameraApp:
    def __init__(self):
        self.cap = None
        self.running = False
        self.setup_gui()
        
    def setup_gui(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Face Password - Camera Control")
        self.root.geometry("400x300")
        
        # Create buttons
        btn_start = tk.Button(
            self.root,
            text="Start Camera",
            command=self.start_camera,
            bg="green",
            fg="white",
            width=20,
            height=2,
            font=("Arial", 12)
        )
        btn_start.pack(pady=10)
        
        btn_stop = tk.Button(
            self.root,
            text="Stop Camera",
            command=self.stop_camera,
            bg="red",
            fg="white",
            width=20,
            height=2,
            font=("Arial", 12)
        )
        btn_stop.pack(pady=10)
        
        btn_capture = tk.Button(
            self.root,
            text="Capture Face",
            command=self.capture_face,
            bg="blue",
            fg="white",
            width=20,
            height=2,
            font=("Arial", 12)
        )
        btn_capture.pack(pady=10)
        
        btn_exit = tk.Button(
            self.root,
            text="Exit",
            command=self.exit_app,
            bg="gray",
            fg="white",
            width=20,
            height=2,
            font=("Arial", 12)
        )
        btn_exit.pack(pady=10)
        
    def start_camera(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.running = True
                # Run camera in separate thread
                thread = threading.Thread(target=self.camera_loop)
                thread.daemon = True
                thread.start()
                messagebox.showinfo("Success", "Camera started!")
            else:
                messagebox.showerror("Error", "Could not open camera")
        else:
            messagebox.showinfo("Info", "Camera is already running")
    
    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Info", "Camera stopped")
    
    def capture_face(self):
        if self.cap and self.cap.isOpened():
            messagebox.showinfo("Capture", "Face capture functionality - to be implemented")
        else:
            messagebox.showwarning("Warning", "Please start camera first")
    
    def camera_loop(self):
        while self.running:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    cv2.imshow('Camera Feed', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.running = False
                        break
    
    def exit_app(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.quit()
    
    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = CameraApp()
    app.run()

