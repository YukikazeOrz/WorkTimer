import tkinter as tk
from tkinter import messagebox
import time
import threading

class WorkReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Work Reminder")
        
        self.work_interval = 25  # Work duration in minutes
        self.rest_interval = 5   # Rest duration in minutes
        
        self.is_running = False
        self.create_widgets()

    def create_widgets(self):
        # Label
        self.label = tk.Label(self.root, text="Work Reminder Tool", font=("Arial", 14))
        self.label.pack(pady=20)

        # Input for work interval
        self.work_label = tk.Label(self.root, text="Work duration (minutes):")
        self.work_label.pack()
        self.work_entry = tk.Entry(self.root)
        self.work_entry.insert(0, str(self.work_interval))
        self.work_entry.pack(pady=5)

        # Input for rest interval
        self.rest_label = tk.Label(self.root, text="Rest duration (minutes):")
        self.rest_label.pack()
        self.rest_entry = tk.Entry(self.root)
        self.rest_entry.insert(0, str(self.rest_interval))
        self.rest_entry.pack(pady=5)

        # Start button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_reminder)
        self.start_button.pack(pady=10)
        
        # Stop button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_reminder)
        self.stop_button.pack(pady=5)

    def start_reminder(self):
        if not self.is_running:
            self.work_interval = int(self.work_entry.get())
            self.rest_interval = int(self.rest_entry.get())
            self.is_running = True
            self.thread = threading.Thread(target=self.run_reminder)
            self.thread.start()

    def stop_reminder(self):
        self.is_running = False

    def run_reminder(self):
        while self.is_running:
            # Work phase
            self.show_message("Work Reminder", f"Time to work for {self.work_interval} minutes!")
            time.sleep(self.work_interval * 60)  # Wait for work interval to complete
            
            if not self.is_running:
                break

            # Rest phase
            self.show_message("Rest Reminder", f"Time to rest for {self.rest_interval} minutes!")
            time.sleep(self.rest_interval * 60)  # Wait for rest interval to complete

    def show_message(self, title, message):
        # Show popup reminder
        messagebox.showinfo(title, message)

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = WorkReminderApp(root)
    root.mainloop()

