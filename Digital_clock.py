import tkinter as tk
from tkinter import messagebox
from time import strftime

alarm_time = None

def update_time():
    global alarm_time
    time_string = strftime('%I:%M:%S %p')
    date_string = strftime('%A, %B %d, %Y')
    lbl.config(text=time_string)
    date_lbl.config(text=date_string)
    
    if alarm_time == time_string:
        alarm_time = None
        alarm_status_lbl.config(text="Alarm: Not set", fg=FG_DATE)
        set_alarm_btn.config(text="SET", bg=FG_TIME)
        # Trigger the alarm message
        messagebox.showinfo("Alarm", "Time's up!")
        
    lbl.after(1000, update_time)

def toggle_alarm():
    global alarm_time
    if alarm_time is None:
        h = hour_var.get().zfill(2)
        m = minute_var.get().zfill(2)
        ampm = ampm_var.get().upper()
        alarm_time = f"{h}:{m}:00 {ampm}"
        alarm_status_lbl.config(text=f"Alarm set for: {h}:{m} {ampm}", fg=ACCENT_COLOR)
        set_alarm_btn.config(text="CANCEL", bg='#FF3333')
    else:
        alarm_time = None
        alarm_status_lbl.config(text="Alarm: Not set", fg=FG_DATE)
        set_alarm_btn.config(text="SET", bg=FG_TIME)

root = tk.Tk()
root.title("Digital Clock")

# -- STYLING TOKENS --
BG_COLOR = '#0F0F11'           # Deep, almost black background
FG_TIME = '#00FFCC'            # Vibrant neon cyan for time
FG_DATE = '#A8B2C1'            # Soft gray-blue for date
ACCENT_COLOR = '#FF0055'       # Neon pink for active alarm status
FRAME_BG = '#1A1A24'           # Slightly lighter background for the alarm section
FONT_MAIN = ('Segoe UI', 80, 'bold')
FONT_DATE = ('Segoe UI', 22)
FONT_ALARM = ('Segoe UI', 14)

root.configure(background=BG_COLOR)
root.resizable(False, False)

# Main frame to hold everything and provide breathing room
main_frame = tk.Frame(root, bg=BG_COLOR, padx=40, pady=30)
main_frame.pack(expand=True, fill='both')

# Time label widget
lbl = tk.Label(main_frame, font=FONT_MAIN, background=BG_COLOR, foreground=FG_TIME)
lbl.pack(anchor='center')

# Date label widget
date_lbl = tk.Label(main_frame, font=FONT_DATE, background=BG_COLOR, foreground=FG_DATE)
date_lbl.pack(anchor='center', pady=(0, 40))

# Alarm UI inside a stylish frame box
alarm_frame = tk.Frame(main_frame, bg=FRAME_BG, padx=15, pady=15, highlightbackground='#333344', highlightthickness=1)
alarm_frame.pack(pady=(0, 15))

alarm_label = tk.Label(alarm_frame, text="SET ALARM:", font=('Segoe UI', 12, 'bold'), bg=FRAME_BG, fg='#FFFFFF')
alarm_label.pack(side=tk.LEFT, padx=(0, 10))

hours = tuple(f"{i:02d}" for i in range(1, 13))
mins_secs = tuple(f"{i:02d}" for i in range(60))

hour_var = tk.StringVar(value="12")
minute_var = tk.StringVar(value="00")
ampm_var = tk.StringVar(value="AM")

# Shared configuration for spinboxes to look modern
spinbox_config = {
    'font': FONT_ALARM, 
    'bg': '#2A2A38', 
    'fg': FG_TIME, 
    'width': 3, 
    'relief': 'flat',
    'highlightthickness': 0,
    'buttonbackground': '#2A2A38'
}

hour_spin = tk.Spinbox(alarm_frame, values=hours, textvariable=hour_var, **spinbox_config)
hour_spin.pack(side=tk.LEFT, padx=3)

tk.Label(alarm_frame, text=":", font=FONT_ALARM, bg=FRAME_BG, fg=FG_TIME).pack(side=tk.LEFT)

minute_spin = tk.Spinbox(alarm_frame, values=mins_secs, textvariable=minute_var, **spinbox_config)
minute_spin.pack(side=tk.LEFT, padx=3)

ampm_spin = tk.Spinbox(alarm_frame, values=("AM", "PM"), textvariable=ampm_var, font=FONT_ALARM, bg='#2A2A38', fg=FG_TIME, width=4, relief='flat', highlightthickness=0, buttonbackground='#2A2A38')
ampm_spin.pack(side=tk.LEFT, padx=5)

# Stylish solid button
set_alarm_btn = tk.Button(alarm_frame, text="SET", font=('Segoe UI', 11, 'bold'), command=toggle_alarm, bg=FG_TIME, fg='#000000', relief='flat', activebackground='#00CCAA', activeforeground='black', padx=15, pady=2)
set_alarm_btn.pack(side=tk.LEFT, padx=(10, 0))

# Alarm status label
alarm_status_lbl = tk.Label(main_frame, text="Alarm: Not set", font=('Segoe UI', 13, 'italic'), bg=BG_COLOR, fg=FG_DATE)
alarm_status_lbl.pack(pady=(0, 0))

update_time()

# Center the window on the screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root.mainloop()
