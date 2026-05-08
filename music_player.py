import os
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# ── Audio Engine (Windows Built-in) ──────────────────────────────────────────
class AudioEngine:
    winmm = ctypes.windll.winmm

    @classmethod
    def send(cls, command):
        buffer = ctypes.create_unicode_buffer(512)
        error_code = cls.winmm.mciSendStringW(str(command), buffer, 511, 0)
        return error_code, buffer.value

    @classmethod
    def play(cls, file_path):
        cls.stop()
        err, _ = cls.send(f'open "{file_path}" type mpegvideo alias music')
        if err != 0:
            err, _ = cls.send(f'open "{file_path}" alias music')
        
        if err == 0:
            cls.send("play music")
            return True
        return False

    @classmethod
    def pause(cls):
        cls.send("pause music")

    @classmethod
    def resume(cls):
        cls.send("resume music")

    @classmethod
    def stop(cls):
        cls.send("stop music")
        cls.send("close music")

# ── UI Constants & Design System ─────────────────────────────────────────────
COLORS = {
    "bg": "#0F0F1A",        # Deep space background
    "surface": "#1A1A2E",   # Card background
    "accent": "#7289DA",    # Vibrant blue
    "secondary": "#E94560", # Pink/Red highlight
    "text": "#EAEAEA",      # Crisp white text
    "text_muted": "#A0A0B8",# Muted gray text
    "button": "#16213E",    # Button background
    "hover": "#0F3460"      # Button hover state
}

# ── Custom Components ────────────────────────────────────────────────────────
class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            bg=COLORS["button"],
            fg=COLORS["text"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            activebackground=COLORS["hover"],
            activeforeground="white"
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(bg=COLORS["hover"])

    def on_leave(self, e):
        self.config(bg=COLORS["button"])

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vibe Player")
        self.root.geometry("500x700")
        self.root.configure(bg=COLORS["bg"])
        
        self.playlist = []
        self.current_song_index = None
        self.is_paused = False

        # --- HEADER ---
        header_frame = tk.Frame(root, bg=COLORS["bg"])
        header_frame.pack(fill="x", pady=30)
        
        tk.Label(header_frame, text="VIBE PLAYER", font=("Inter", 24, "bold"), 
                 bg=COLORS["bg"], fg=COLORS["secondary"]).pack()
        tk.Label(header_frame, text="YOUR PERSONAL SOUNDSCAPE", font=("Inter", 8, "bold"), 
                 bg=COLORS["bg"], fg=COLORS["text_muted"]).pack()

        # --- NOW PLAYING DISPLAY ---
        np_frame = tk.Frame(root, bg=COLORS["surface"], highlightthickness=1, highlightbackground="#252540")
        np_frame.pack(padx=30, pady=30, fill="x")
        
        self.song_label = tk.Label(np_frame, text="Pick a track to start the vibe", 
                                   font=("Segoe UI", 12, "bold"), 
                                   bg=COLORS["surface"], fg=COLORS["text"], wraplength=400)
        self.song_label.pack()
        
        self.status_label = tk.Label(np_frame, text="IDLE", font=("Segoe UI", 8, "bold"), 
                                     bg=COLORS["surface"], fg=COLORS["text_muted"])
        self.status_label.pack(pady=(10, 0))

        # --- PLAYLIST SECTION ---
        list_label_frame = tk.Frame(root, bg=COLORS["bg"])
        list_label_frame.pack(fill="x", padx=30, pady=(30, 5))
        tk.Label(list_label_frame, text="PLAYLIST", font=("Segoe UI", 9, "bold"), 
                 bg=COLORS["bg"], fg=COLORS["text_muted"]).pack(side="left")

        self.listbox = tk.Listbox(
            root, 
            bg=COLORS["surface"], 
            fg=COLORS["text"], 
            selectbackground=COLORS["accent"], 
            font=("Segoe UI", 10),
            width=50, height=12, border=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.listbox.pack(padx=30, pady=5, fill="both", expand=True)

        # --- CONTROLS (Centered Cluster) ---
        ctrl_frame = tk.Frame(root, bg=COLORS["bg"])
        ctrl_frame.pack(fill="x", pady=20)
        
        # --- CONTROLS (Centered Cluster) ---
        ctrl_frame = tk.Frame(root, bg=COLORS["bg"])
        ctrl_frame.pack(fill="x", pady=20)
        
        # Inner container using Grid for better resizing
        inner_ctrl = tk.Frame(ctrl_frame, bg=COLORS["bg"])
        inner_ctrl.pack(anchor="center")

        # Configure columns to be equal
        for i in range(5):
            inner_ctrl.grid_columnconfigure(i, weight=1, uniform="equal")

        ModernButton(inner_ctrl, text="⏮ PREV", command=self.play_prev, width=8).grid(row=0, column=0, padx=5)
        self.play_btn = ModernButton(inner_ctrl, text="▶ PLAY", command=self.play_selected, width=12, bg=COLORS["secondary"])
        self.play_btn.grid(row=0, column=1, padx=10)
        self.pause_btn = ModernButton(inner_ctrl, text="⏸ PAUSE", command=self.toggle_pause, width=8)
        self.pause_btn.grid(row=0, column=2, padx=5)
        ModernButton(inner_ctrl, text="⏹ STOP", command=self.stop_music, width=8).grid(row=0, column=3, padx=5)
        ModernButton(inner_ctrl, text="⏭ NEXT", command=self.play_next, width=8).grid(row=0, column=4, padx=5)

        # --- FOOTER ---
        footer_frame = tk.Frame(root, bg=COLORS["bg"])
        footer_frame.pack(fill="x", pady=20)
        
        ModernButton(footer_frame, text="📂 LOAD MUSIC", command=self.load_folder, 
                    bg=COLORS["accent"]).pack()

    def load_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.playlist = [os.path.join(folder, f) for f in os.listdir(folder) 
                             if f.lower().endswith(('.mp3', '.wav'))]
            self.listbox.delete(0, tk.END)
            for path in self.playlist:
                name = os.path.basename(path)
                self.listbox.insert(tk.END, f"  {name}")
            
            if not self.playlist:
                messagebox.showwarning("Empty", "No audio files found in this folder.")

    def play_selected(self):
        selection = self.listbox.curselection()
        if selection:
            self.current_song_index = selection[0]
            path = self.playlist[self.current_song_index]
            self._start_playback(path)
        elif self.playlist and self.current_song_index is None:
            self.current_song_index = 0
            self._start_playback(self.playlist[0])

    def _start_playback(self, path):
        if AudioEngine.play(path):
            name = os.path.basename(path).upper()
            self.song_label.config(text=name)
            self.status_label.config(text="PLAYING", fg=COLORS["accent"])
            self.play_btn.config(text="▶ PLAYING")
            self.pause_btn.config(text="⏸ PAUSE")
            self.is_paused = False
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_song_index)
        else:
            messagebox.showerror("Error", "Codec Error: Windows cannot decode this MP3.")

    def toggle_pause(self):
        if self.current_song_index is not None:
            if self.is_paused:
                AudioEngine.resume()
                self.is_paused = False
                self.status_label.config(text="PLAYING", fg=COLORS["accent"])
                self.pause_btn.config(text="⏸ PAUSE")
            else:
                AudioEngine.pause()
                self.is_paused = True
                self.status_label.config(text="PAUSED", fg="#F1C40F")
                self.pause_btn.config(text="▶ RESUME")

    def stop_music(self):
        AudioEngine.stop()
        self.song_label.config(text="VIBE CHECK COMPLETE")
        self.status_label.config(text="STOPPED", fg=COLORS["text_muted"])
        self.play_btn.config(text="▶ PLAY")
        self.pause_btn.config(text="⏸ PAUSE")
        self.current_song_index = None
        self.listbox.selection_clear(0, tk.END)

    def play_next(self):
        if self.playlist:
            if self.current_song_index is None:
                self.current_song_index = 0
            else:
                self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self._start_playback(self.playlist[self.current_song_index])

    def play_prev(self):
        if self.playlist:
            if self.current_song_index is None:
                self.current_song_index = len(self.playlist) - 1
            else:
                self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self._start_playback(self.playlist[self.current_song_index])

if __name__ == "__main__":
    root = tk.Tk()
    # Center the window and set min size
    w, h = 500, 750
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    root.minsize(500, 750) # Prevent layout breaking when too small
    
    app = MusicPlayerApp(root)
    root.mainloop()
    AudioEngine.stop()
