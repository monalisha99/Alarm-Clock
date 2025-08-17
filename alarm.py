
# Import necessary modules
import tkinter as tk                            
from tkinter import messagebox                  
from datetime import datetime                   # For current date/time
import time                                     # For sleep
import threading                                # To run alarm without freezing GUI
import subprocess                               # To run system commands (play audio)

# Global variables to manage alarm thread
running = True
alarm_thread = None

# ----------------------- FUNCTION TO UPDATE LIVE CLOCK -----------------------
def update_clock():
    current_time = datetime.now().strftime("%I:%M:%S %p")  # Format current time (e.g., 08:45:01 PM)
    current_day = datetime.now().strftime("%A")            # Get full day name (e.g., "Tuesday")

    # Update the labels with current time and day
    live_clock_label.config(text=current_time)
    live_day_label.config(text=current_day)

    # Call this function again after 1 second (1000 milliseconds)
    root.after(1000, update_clock)


# ----------------------- FUNCTION TO SET ALARM -----------------------
def set_alarm():
    global running, alarm_thread
    running = True                                          # Enable alarm loop
    alarm_time = entry_time.get()                           # Get the alarm time entered by user
    label.config(text=f"Alarm set for {alarm_time}")        # Show alarm time on screen

    # Function to run in separate thread
    def alarm():
        try:
            while running:
                now = datetime.now()
                current_time = now.strftime("%I:%M %p").strip().upper()     # Format: "08:30 PM"
                current_day = now.strftime("%A")                            # e.g., "Monday"
                alarm_time_clean = alarm_time.strip().upper()              # Clean user input

                # Check: if current time == alarm time and the selected day matches
                if current_time == alarm_time_clean and days_selected.get(current_day, tk.BooleanVar()).get():
                    subprocess.run(["mpg123", "alarm_clock.mp3"])          # Play alarm sound (Linux)
                    messagebox.showinfo("Alarm", "Wake Up!")               # Show popup
                    break
                time.sleep(1)                                              # Wait 1 second before checking again
        except:
            messagebox.showerror("Error", "Something is wrong!")           # Show error popup

    # Start the alarm thread
    alarm_thread = threading.Thread(target=alarm)
    alarm_thread.start()


# ----------------------- FUNCTION TO TURN OFF ALARM -----------------------
def off_alarm():
    global running
    running = False                                # Stop alarm loop
    label.config(text="Alarm Stopped")             # Show status on screen
    subprocess.run(["pkill", "mpg123"])            # Kill audio process (Linux specific)


# ----------------------- GUI SETUP -----------------------
root = tk.Tk()
root.title("Alarm Clock")                          # Title of the window
root.configure(bg="white")                         # Background color
root.geometry("640x380")                           # Window size

# Live Day Label
live_day_label = tk.Label(root, font=("Arial, 24"), fg="blue", bg="white")
live_day_label.pack(pady=10)

# Live Clock Label
live_clock_label = tk.Label(root, font=("Arial, 24"), fg="blue", bg="white")
live_clock_label.pack(pady=10)

# Label for alarm setting
label = tk.Label(root, text="Set time", font=("Arial", 14), fg="blue", bg="white")
label.pack(pady=10)

# Time Entry field
entry_time = tk.Entry(root, font=("Arial, 24"), width=30, justify="center")
entry_time.insert(0, "00:00 AM")                   # Default value
entry_time.pack(pady=10, ipady=10)

# Empty frame (for future use if needed)
frame = tk.Frame(root)
frame.pack(pady=5)

# ON Button
on_button = tk.Button(root, 
                      text="ON", 
                      font=("Arial", 16), 
                      fg="black", 
                      bg="lightblue", 
                      activebackground="blue", 
                      activeforeground="white", 
                      command=set_alarm)           # Calls set_alarm
on_button.pack(pady=10, ipady=5)

# OFF Button
off_button = tk.Button(root, 
                       text="OFF", 
                       font=("Arial", 16), 
                       bg="lightblue", 
                       fg="black", 
                       activebackground="blue", 
                       activeforeground="red", 
                       command=off_alarm)          # Calls off_alarm
off_button.pack(pady=10, ipadx=2)


# ----------------------- DAY SELECTION CHECKBOXES -----------------------
days_selected = {}                                 # Dictionary to store each day's BooleanVar
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Label for day selection
tk.Label(root, text="Select Day(s) for Alarm:", font=("Arial, 24"), fg="blue", bg="white").pack(pady=5, ipady=10)

# Create a frame to hold checkboxes
checkbox_frame = tk.Frame(root, bg="white")
checkbox_frame.pack(pady=10)

# Add a checkbox for each day
for i, day in enumerate(days):
    var = tk.BooleanVar()                           # Variable to hold checkbox value
    chk = tk.Checkbutton(checkbox_frame, 
                         text=day, 
                         variable=var, 
                         font=("Arial", 14),
                         fg="blue",
                         bg="lightgray",
                         activeforeground="red", 
                         width=15,                  # Width of checkbox text
                         anchor="w",                # Left align text
                         padx=10)                   # Padding
    chk.grid(row=i, column=0, sticky="w", padx=20, pady=10, ipady=2)

    days_selected[day] = var                        # Save variable to dictionary


# ----------------------- START CLOCK AND MAINLOOP -----------------------
update_clock()                                     # Start updating time
root.mainloop()                                    # Start GUI event loop
