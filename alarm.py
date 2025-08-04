import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import threading
import subprocess

def set_alarm():
    alarm_time = entry_time.get()
    label.config(text=f"Alarm set for {alarm_time}")
    
    def alarm():
        try:
            while True:
                current_time = datetime.now().strftime("%H:%M")
                if current_time == alarm_time:
                    subprocess.run(["mpg123", "alarm_clock.mp3"])  # For Linux
                    messagebox.showinfo("Alarm", "Wake Up!")
                    break
                time.sleep(1)
        except:
            messagebox.showerror("Error", "Something is wrong!")

    threading.Thread(target=alarm).start() 

# Tkinter GUI
root = tk.Tk()
root.title("Alarm Clock")
root.geometry("640x380")

label = tk.Label(root, text="Set time", font=("Arial", 14), fg="blue")
label.pack(pady=10)

entry_time = tk.Entry(root)
entry_time.insert(0, "00:00")  
entry_time.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

play_button = tk.Button(root, 
                        text="Play", 
                        font=("Arial", 16), 
                        fg="black", 
                        bg="lightblue", 
                        activebackground="blue", 
                        activeforeground="white", 
                        command=set_alarm)
play_button.pack(pady=10)

off_button = tk.Button(root, 
                       text="Off", 
                       font=("Arial", 16), 
                       bg="lightgray", 
                       fg="white", 
                       activebackground="gray", 
                       activeforeground="red")
off_button.pack(pady=10)

root.mainloop()
