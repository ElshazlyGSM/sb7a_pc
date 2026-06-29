import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TasbeehTimerApp:
    def __init__(self, root):
        self.root = root
        root.title("سبحة")
        root.geometry("380x320")
        root.attributes("-topmost", True)
        root.resizable(False, False)

        self.count = 0
        self.timer_running = False
        self.interval_seconds = 1
        self.timer_id = None
        self.compact_mode = False
        self.topmost_var = tk.BooleanVar(value=True)
        self.zikr_name_var = tk.StringVar(value="اسم الذكر هنا")
        self.drag_data = {"x": 0, "y": 0}

        self.build_ui()
        self.update_topmost()

    def build_ui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(self.main_frame, text="سبحة", font=("Arial", 18, "bold"))
        title_label.pack(pady=(10, 4))

        entry_frame = ttk.Frame(self.main_frame)
        entry_frame.pack(pady=6, fill="x", padx=14)

        ttk.Label(entry_frame, text="اسم الذكر:", width=10).pack(side="left")
        self.zikr_name_entry = ttk.Entry(entry_frame, textvariable=self.zikr_name_var)
        self.zikr_name_entry.pack(side="left", fill="x", expand=True)

        self.counter_frame = ttk.Frame(self.main_frame)
        self.counter_frame.pack(pady=12, padx=14, fill="both", expand=True)

        self.count_label = ttk.Label(self.counter_frame, text=str(self.count), font=("Arial", 48, "bold"), foreground="#0B6623")
        self.count_label.pack(pady=8)

        self.display_label = ttk.Label(self.counter_frame, text="اضغط زر العد أو شغّل المؤقت", font=("Arial", 12))
        self.display_label.pack()

        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.pack(pady=10, fill="x", padx=14)

        self.manual_button = ttk.Button(controls_frame, text="تسبيح يدوي", command=self.increment_count)
        self.manual_button.pack(fill="x")

        timer_control_frame = ttk.Frame(self.main_frame)
        timer_control_frame.pack(pady=10, fill="x", padx=14)

        ttk.Label(timer_control_frame, text="كل (ثانية):").pack(side="left")
        self.interval_entry = ttk.Entry(timer_control_frame, width=6)
        self.interval_entry.insert(0, str(self.interval_seconds))
        self.interval_entry.pack(side="left", padx=(4, 8))

        self.start_button = ttk.Button(timer_control_frame, text="تشغيل المؤقت", command=self.toggle_timer)
        self.start_button.pack(side="left", fill="x", expand=True)

        option_frame = ttk.Frame(self.main_frame)
        option_frame.pack(pady=8, fill="x", padx=14)

        topmost_check = ttk.Checkbutton(option_frame, text="تبقى فوق كل النوافذ", variable=self.topmost_var, command=self.update_topmost)
        topmost_check.pack(side="left", anchor="w")

        self.compact_button = ttk.Button(option_frame, text="عرض مصغّر", command=self.toggle_compact_mode)
        self.compact_button.pack(side="right")

        self.reset_button = ttk.Button(self.main_frame, text="إعادة ضبط", command=self.reset_count)
        self.reset_button.pack(padx=14, fill="x")

        footer = ttk.Label(self.main_frame, text="اسحب العداد لتحريكه، اضغط عرض مصغّر فقط للعداد", font=("Arial", 10, "italic"))
        footer.pack(pady=(8, 0))

        self.compact_frame = ttk.Frame(self.root)
        self.compact_count_label = ttk.Label(self.compact_frame, text=str(self.count), font=("Arial", 32, "bold"), foreground="#0B6623")
        self.compact_count_label.pack(padx=6, pady=(6, 0))

        compact_button_row = ttk.Frame(self.compact_frame)
        compact_button_row.pack(padx=10, pady=(8, 6))

        self.compact_toggle_button = ttk.Button(compact_button_row, text="إيقاف" if self.timer_running else "تشغيل", command=self.toggle_timer, width=8)
        self.compact_toggle_button.pack(side="left", padx=(0, 4))

        self.compact_exit_button = ttk.Button(compact_button_row, text="عودة", command=self.exit_compact_mode, width=8)
        self.compact_exit_button.pack(side="left")

        self.root.bind("<Escape>", lambda event: self.exit_compact_mode())
        self.count_label.bind("<ButtonPress-1>", self.start_move)
        self.count_label.bind("<B1-Motion>", self.on_move)
        self.compact_frame.bind("<ButtonPress-1>", self.start_move)
        self.compact_frame.bind("<B1-Motion>", self.on_move)
        self.compact_count_label.bind("<ButtonPress-1>", self.start_move)
        self.compact_count_label.bind("<B1-Motion>", self.on_move)
        self.compact_count_label.bind("<Double-Button-1>", lambda event: self.toggle_compact_mode())

    def increment_count(self):
        self.count += 1
        self.update_count_display()

    def update_count_display(self):
        self.count_label.config(text=str(self.count))
        self.compact_count_label.config(text=str(self.count))
        self.update_compact_toggle_text()
        zikr_name = self.zikr_name_var.get().strip() or "ذكر"
        self.display_label.config(text=f"{zikr_name} - العدد: {self.count}")

    def update_compact_toggle_text(self):
        if hasattr(self, 'compact_toggle_button'):
            self.compact_toggle_button.config(text="إيقاف" if self.timer_running else "تشغيل")

    def reset_count(self):
        self.count = 0
        self.update_count_display()

    def toggle_timer(self):
        if self.timer_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        try:
            seconds = float(self.interval_entry.get())
            if seconds <= 0:
                raise ValueError
            self.interval_seconds = seconds
        except ValueError:
            messagebox.showerror("خطأ", "اكتب رقم صحيح أكبر من صفر لعدد الثواني")
            return

        self.timer_running = True
        self.start_button.config(text="إيقاف المؤقت")
        self.interval_entry.config(state="disabled")
        self.schedule_tick()
        self.enter_compact_mode()
        self.update_compact_toggle_text()

    def stop_timer(self):
        if not self.timer_running:
            return
        self.timer_running = False
        self.start_button.config(text="تشغيل المؤقت")
        self.interval_entry.config(state="normal")
        self.update_compact_toggle_text()
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def schedule_tick(self):
        if self.timer_running:
            self.increment_count()
            self.timer_id = self.root.after(int(self.interval_seconds * 1000), self.schedule_tick)

    def update_topmost(self):
        self.root.attributes("-topmost", self.topmost_var.get())

    def toggle_compact_mode(self):
        self.compact_mode = not self.compact_mode
        if self.compact_mode:
            self.enter_compact_mode()
        else:
            self.exit_compact_mode()

    def enter_compact_mode(self):
        self.compact_mode = True
        self.main_frame.pack_forget()
        self.root.overrideredirect(True)
        self.compact_button.config(text="عرض كامل")
        self.compact_frame.pack(fill="both", expand=True)
        self.root.geometry("150x100")
        self.update_topmost()

    def exit_compact_mode(self):
        if not self.compact_mode:
            return
        self.compact_mode = False
        self.compact_frame.pack_forget()
        self.root.overrideredirect(False)
        self.main_frame.pack(fill="both", expand=True)
        self.compact_button.config(text="عرض مصغّر")
        self.root.geometry("380x320")
        self.update_topmost()

    def start_move(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_move(self, event):
        x = self.root.winfo_x() + event.x - self.drag_data["x"]
        y = self.root.winfo_y() + event.y - self.drag_data["y"]
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TasbeehTimerApp(root)
    root.mainloop()
