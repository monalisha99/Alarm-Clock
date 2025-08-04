

import tkinter as tk
from datetime import datetime

def update_clock():
    current_time = datetime.now().strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
    current_day = datetime.now().strftime("%A")            # Full weekday name

    clock_label.config(text=current_time)
    day_label.config(text=current_day)

    root.after(1000, update_clock)  # update every second

root = tk.Tk()
root.title("Live Clock with Day")
root.geometry("350x200")
root.configure(bg="black")

# Day label (e.g., Monday)
day_label = tk.Label(root, font=("Arial", 20), fg="lightgreen", bg="black")
day_label.pack(pady=10)

# Time label (e.g., 11:34:56 AM)
clock_label = tk.Label(root, font=("Arial", 36), fg="cyan", bg="black")
clock_label.pack(pady=10)

update_clock()
root.mainloop()


