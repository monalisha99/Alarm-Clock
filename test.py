import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time

root = tk.Tk()
root.title("Weekday Alarm Clock")
root.geometry("400x400")

# ==== Entry for alarm time ====
tk.Label(root, text="Set Alarm Time (HH:MM)").pack(pady=5)
entry_time = tk.Entry(root, font=("Arial", 16), justify="center")
entry_time.insert(0, "07:00")
entry_time.pack(pady=5)

# ==== Checkboxes for days ====
days_selected = {}  # Dictionary to store each day's BooleanVar

tk.Label(root, text="Select Day(s) for Alarm:").pack(pady=5)

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for day in days:
    var = tk.BooleanVar()
    chk = tk.Checkbutton(root, text=day, variable=var)
    chk.pack(anchor='w', padx=20)
    days_selected[day] = var

# ==== Alarm checking logic ====
def alarm_check():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A")
        
        if current_time == entry_time.get() and days_selected[current_day].get():
            messagebox.showinfo("Alarm", f"⏰ Alarm for {current_day} at {current_time}!")
            time.sleep(60)  # Wait 60s so it doesn't repeat within the same minute
        time.sleep(1)

def start_alarm_thread():
    t = threading.Thread(target=alarm_check)
    t.daemon = True
    t.start()

start_alarm_thread()

# ==== Display current time and day ====
clock_label = tk.Label(root, font=("Arial", 20))
clock_label.pack(pady=10)

day_label = tk.Label(root, font=("Arial", 14))
day_label.pack()

def update_clock():
    now = datetime.now()
    clock_label.config(text=now.strftime("%I:%M:%S %p"))
    day_label.config(text=now.strftime("%A"))
    root.after(1000, update_clock)

update_clock()
root.mainloop()
