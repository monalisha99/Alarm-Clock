import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import threading
import subprocess


running = True
alarm_thread = None


def update_clock():
    current_time = datetime.now().strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
    current_day = datetime.now().strftime("%A")            # Full weekday name

    live_clock_label.config(text=current_time)
    live_day_label.config(text=current_day)

    root.after(1000, update_clock)  # update every second



def set_alarm():
    global running, alarm_thread
    running = True
    alarm_time = entry_time.get()
    label.config(text=f"Alarm set for {alarm_time}")
    
    def alarm():
        try:
            while running:
                now = datetime.now()
                current_time = now.strftime("%I:%M %p").strip().upper()
                current_day = now.strftime("%A")  # e.g., "Monday"

                alarm_time_clean = alarm_time.strip().upper()

                # ✅ Check both time and day match
                if current_time == alarm_time_clean and days_selected.get(current_day, tk.BooleanVar()).get():
                    subprocess.run(["mpg123", "alarm_clock.mp3"])  # For Linux
                    messagebox.showinfo("Alarm", "Wake Up!")
                    break
                time.sleep(1)
        except:
            messagebox.showerror("Error", "Something is wrong!")

    alarm_thread = threading.Thread(target=alarm)
    alarm_thread.start()



def off_alarm():
    global running
    running = False
    label.config(text="Alarm Stopped")
    subprocess.run(["pkill", "mpg123"])    # works on linux to kill music




# Tkinter GUI
root = tk.Tk()
root.title("Alarm Clock")
root.configure(bg="black")
root.geometry("640x380")


live_day_label = tk.Label(root, font=("Arial, 24"), fg="blue", bg="black")
live_day_label.pack(pady=10)

live_clock_label = tk.Label(root, font=("Arial, 24"), fg="blue", bg="black")
live_clock_label.pack(pady=10)

label = tk.Label(root, text="Set time", font=("Arial", 14), fg="blue", bg="black")
label.pack(pady=10)

entry_time = tk.Entry(root, font=("Arial, 24"), width=30, justify="center")
entry_time.insert(0, "00:00 AM")  
entry_time.pack(pady=10, ipady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

on_button = tk.Button(root, 
                        text="ON", 
                        font=("Arial", 16), 
                        fg="black", 
                        bg="lightblue", 
                        activebackground="blue", 
                        activeforeground="white", 
                        command=set_alarm)
on_button.pack(pady=10, ipady=5)

off_button = tk.Button(root, 
                       text="OFF", 
                       font=("Arial", 16), 
                       bg="lightblue", 
                       fg="black", 
                       activebackground="blue", 
                       activeforeground="red", 
                       command=off_alarm)
off_button.pack(pady=10, ipadx=2)


days_selected = {}  # Dictionary to store each day's BooleanVar
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

tk.Label(root, text="Select Day(s) for Alarm:", font=("Arial, 24"), fg="blue", bg="black").pack(pady=5, ipady=10)

# Create a frame for checkboxes
checkbox_frame = tk.Frame(root, bg="black")
checkbox_frame.pack(pady=10)

# Place checkboxes in two columns
for i, day in enumerate(days):
    var = tk.BooleanVar()
    chk = tk.Checkbutton(checkbox_frame, 
                         text=day, 
                         variable=var, 
                         font=("Arial", 14),
                         fg="blue",
                         bg="black", 
                         width=15,         
                         anchor="w",        
                         padx=10)
    chk.grid(row=i, column=0, sticky="w", padx=20, pady=10, ipady=2)
    
    # ✅ Store the variable in the dictionary
    days_selected[day] = var
update_clock()
root.mainloop()
