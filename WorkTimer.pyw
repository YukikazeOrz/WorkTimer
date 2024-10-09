import tkinter as tk
from tkinter import ttk
import time
import threading
import winsound

class WorkReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Work Reminder")
        self.root.geometry("800x800")  # 窗口大小

        # 设置 DPI 缩放适配
        self.root.tk.call('tk', 'scaling', 2)  # 调整为合适的比例（1.5 可根据需要调整）

        self.work_minutes = 25  # 工作时间默认为25分钟
        self.work_seconds = 0
        self.rest_minutes = 5    # 休息时间默认为5分钟
        self.rest_seconds = 0
        
        self.is_running = False
        self.remaining_time = 0
        self.stop_event = threading.Event()
        
        # 创建标签页
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.setup_tab = ttk.Frame(self.notebook)
        self.display_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.setup_tab, text='设置倒计时')
        self.notebook.add(self.display_tab, text='展示倒计时')

        self.create_setup_widgets()
        self.create_display_widgets()

    def create_setup_widgets(self):
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 14), padding=10)
        self.style.configure("TLabel", font=("Segoe UI", 14), padding=5)

        # 工作时间设置
        self.work_label = ttk.Label(self.setup_tab, text="工作时间 (分钟:秒):", font=("Segoe UI", 16, "bold"))
        self.work_label.pack(pady=10)

        work_frame = ttk.Frame(self.setup_tab)
        work_frame.pack(pady=5)

        self.work_minutes_combo = ttk.Combobox(work_frame, values=list(range(0, 61)), state='readonly', width=5)
        self.work_minutes_combo.set(self.work_minutes)
        self.work_minutes_combo.pack(side='left', padx=5)

        self.work_seconds_combo = ttk.Combobox(work_frame, values=list(range(0, 60)), state='readonly', width=5)
        self.work_seconds_combo.set(self.work_seconds)
        self.work_seconds_combo.pack(side='left', padx=5)

        # 休息时间设置
        self.rest_label = ttk.Label(self.setup_tab, text="休息时间 (分钟:秒):", font=("Segoe UI", 16, "bold"))
        self.rest_label.pack(pady=10)

        rest_frame = ttk.Frame(self.setup_tab)
        rest_frame.pack(pady=5)

        self.rest_minutes_combo = ttk.Combobox(rest_frame, values=list(range(0, 61)), state='readonly', width=5)
        self.rest_minutes_combo.set(self.rest_minutes)
        self.rest_minutes_combo.pack(side='left', padx=5)

        self.rest_seconds_combo = ttk.Combobox(rest_frame, values=list(range(0, 60)), state='readonly', width=5)
        self.rest_seconds_combo.set(self.rest_seconds)
        self.rest_seconds_combo.pack(side='left', padx=5)

        # 切换按钮
        self.toggle_button = ttk.Button(self.setup_tab, text="开始倒计时", command=self.toggle_reminder)
        self.toggle_button.pack(pady=20)

    def create_display_widgets(self):
        self.timer_label = ttk.Label(self.display_tab, text="剩余时间: 0:00", font=("Segoe UI", 16, "bold"))
        self.timer_label.pack(pady=20)

        self.progress = ttk.Progressbar(self.display_tab, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.message_label = ttk.Label(self.display_tab, text="", font=("Segoe UI", 14), foreground="green")
        self.message_label.pack(pady=10)

    def toggle_reminder(self):
        if not self.is_running:
            self.work_minutes = int(self.work_minutes_combo.get())
            self.work_seconds = int(self.work_seconds_combo.get())
            self.rest_minutes = int(self.rest_minutes_combo.get())
            self.rest_seconds = int(self.rest_seconds_combo.get())
            self.is_running = True
            self.toggle_button.config(text="停止倒计时")
            self.stop_event.clear()
            self.notebook.select(self.display_tab)  # 切换到展示倒计时页面
            self.thread = threading.Thread(target=self.run_reminder)
            self.thread.start()
        else:
            self.is_running = False
            self.stop_event.set()
            self.toggle_button.config(text="开始倒计时")
            self.message_label.config(text="")

    def run_reminder(self):
        while self.is_running:
            self.remaining_time = self.work_minutes * 60 + self.work_seconds
            self.update_display("工作")
            if not self.is_running:
                break

            self.remaining_time = self.rest_minutes * 60 + self.rest_seconds
            self.update_display("休息")

    def update_display(self, phase):
        self.progress['maximum'] = self.remaining_time
        self.message_label.config(text=f"现在是{phase}时间!")
        
        while self.remaining_time > 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"剩余时间: {mins}:{secs:02d}")
            self.progress['value'] = self.progress['maximum'] - self.remaining_time
            time.sleep(1)
            self.remaining_time -= 1

        if self.is_running:
            self.play_sound()
            self.message_label.config(text=f"{phase}时间结束!")

    def play_sound(self):
        for freq in [523, 587, 659, 698]:
            winsound.Beep(freq, 250)

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkReminderApp(root)
    root.mainloop()
