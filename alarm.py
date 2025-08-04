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
                current_time = datetime.now().strftime("%I:%M %p")  # 12-hour format
                alarm_time_clean = alarm_time.strip().upper()       #Removes any leading or trailing spaces.
                current_time_clean = current_time.strip().upper()
            
                if current_time_clean == alarm_time_clean:
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

live_day_label = tk.Label(root, font=("Arial,24"), fg="blue")
live_day_label.pack(pady=10)

live_clock_label = tk.Label(root, font=("Arial, 24"), fg="blue")
live_clock_label.pack(pady=10)

label = tk.Label(root, text="Set time", font=("Arial", 14), fg="blue")
label.pack(pady=10)

entry_time = tk.Entry(root, font=("Arial, 24"), width=40, justify="center")
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
on_button.pack(pady=10)

off_button = tk.Button(root, 
                       text="OFF", 
                       font=("Arial", 16), 
                       bg="lightgray", 
                       fg="white", 
                       activebackground="gray", 
                       activeforeground="red", 
                       command=off_alarm)
off_button.pack(pady=10)

update_clock()
root.mainloop()
