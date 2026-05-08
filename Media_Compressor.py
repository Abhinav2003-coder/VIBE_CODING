import os
import subprocess
import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
import math

# Set appearance and theme for a premium feel
ctk.set_appearance_mode("Dark")

# Custom Color Palette
BG_COLOR = "#0F172A"      # Deep Navy
SIDEBAR_COLOR = "#1E293B" # Slate Blue
ACCENT_COLOR = "#6366F1"  # Indigo
SUCCESS_COLOR = "#10B981" # Emerald
ERROR_COLOR = "#EF4444"   # Rose
TEXT_COLOR = "#F8FAFC"    # White Smoke
SECONDARY_TEXT = "#94A3B8" # Slate Gray

class MediaCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Antigravity Media Compressor")
        self.geometry("1000x700")
        self.configure(fg_color=BG_COLOR)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selected_file = None
        self.output_folder = None
        self.file_type = None  # "image" or "video"
        self.is_compressing = False

        self.create_widgets()

    def create_widgets(self):
        # Sidebar for configuration
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=SIDEBAR_COLOR, border_width=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(15, weight=1)

        # Sidebar Hero
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="✨ MEDIA\nCOMPRESSOR", 
                                      font=ctk.CTkFont(size=24, weight="bold"), text_color=TEXT_COLOR)
        self.logo_label.grid(row=0, column=0, padx=30, pady=(40, 10), sticky="w")
        
        self.tagline = ctk.CTkLabel(self.sidebar_frame, text="Optimize your media in seconds.", 
                                   font=ctk.CTkFont(size=12), text_color=SECONDARY_TEXT)
        self.tagline.grid(row=1, column=0, padx=30, pady=(0, 30), sticky="w")

        # Section: Image Settings
        self.img_header = ctk.CTkLabel(self.sidebar_frame, text="🖼️ IMAGE SETTINGS", 
                                      font=ctk.CTkFont(size=13, weight="bold"), text_color=ACCENT_COLOR)
        self.img_header.grid(row=2, column=0, padx=30, pady=(10, 5), sticky="w")

        self.quality_label = ctk.CTkLabel(self.sidebar_frame, text="Quality: 70%", text_color=TEXT_COLOR)
        self.quality_label.grid(row=3, column=0, padx=30, pady=(0, 0), sticky="w")
        
        self.quality_slider = ctk.CTkSlider(self.sidebar_frame, from_=10, to=100, number_of_steps=90,
                                          button_color=ACCENT_COLOR, button_hover_color="#4F46E5", progress_color=ACCENT_COLOR, command=self.update_quality_label)
        self.quality_slider.set(70)
        self.quality_slider.grid(row=4, column=0, padx=30, pady=(5, 15), sticky="ew")

        self.resize_label = ctk.CTkLabel(self.sidebar_frame, text="Scale: 100%", text_color=TEXT_COLOR)
        self.resize_label.grid(row=5, column=0, padx=30, pady=(0, 0), sticky="w")
        
        self.resize_slider = ctk.CTkSlider(self.sidebar_frame, from_=10, to=100, number_of_steps=90,
                                         button_color=ACCENT_COLOR, button_hover_color="#4F46E5", progress_color=ACCENT_COLOR, command=self.update_resize_label)
        self.resize_slider.set(100)
        self.resize_slider.grid(row=6, column=0, padx=30, pady=(5, 25), sticky="ew")

        # Section: Video Settings
        self.vid_header = ctk.CTkLabel(self.sidebar_frame, text="🎬 VIDEO SETTINGS", 
                                      font=ctk.CTkFont(size=13, weight="bold"), text_color=ACCENT_COLOR)
        self.vid_header.grid(row=7, column=0, padx=30, pady=(10, 5), sticky="w")
        
        self.vid_quality_var = ctk.StringVar(value="Medium")
        self.vid_quality_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Low", "Medium", "High"], 
                                                variable=self.vid_quality_var, fg_color="#334155", 
                                                button_color="#334155", button_hover_color="#475569")
        self.vid_quality_menu.grid(row=8, column=0, padx=30, pady=(5, 30), sticky="ew")

        # Main Content Area
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=40, pady=40, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)

        # Drag & Drop Style Card
        self.drop_card = ctk.CTkFrame(self.main_container, height=250, fg_color="#1E293B", border_width=1, border_color="#334155")
        self.drop_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.drop_card.grid_propagate(False)
        self.drop_card.grid_columnconfigure(0, weight=1)
        self.drop_card.grid_rowconfigure(0, weight=1)

        self.select_content = ctk.CTkFrame(self.drop_card, fg_color="transparent")
        self.select_content.grid(row=0, column=0)

        self.icon_label = ctk.CTkLabel(self.select_content, text="📥", font=ctk.CTkFont(size=50))
        self.icon_label.grid(row=0, column=0, pady=(0, 10))

        self.instruction_label = ctk.CTkLabel(self.select_content, text="Select Image or Video", 
                                             font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_COLOR)
        self.instruction_label.grid(row=1, column=0)

        self.select_btn = ctk.CTkButton(self.select_content, text="Browse Files", command=self.select_file, 
                                       fg_color=ACCENT_COLOR, hover_color="#4F46E5", width=160, height=35)
        self.select_btn.grid(row=2, column=0, pady=(20, 0))

        # Info Card
        self.info_card = ctk.CTkFrame(self.main_container, fg_color="#1E293B", border_width=1, border_color="#334155")
        self.info_card.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.info_card.grid_columnconfigure((0, 1), weight=1)

        self.file_label = ctk.CTkLabel(self.info_card, text="No file selected", 
                                      font=ctk.CTkFont(size=15, weight="bold"), text_color=TEXT_COLOR)
        self.file_label.grid(row=0, column=0, columnspan=2, pady=(15, 5))

        self.orig_size_label = ctk.CTkLabel(self.info_card, text="Original Size: -", text_color=SECONDARY_TEXT)
        self.orig_size_label.grid(row=1, column=0, pady=(0, 5))

        self.comp_size_label = ctk.CTkLabel(self.info_card, text="Compressed Size: -", text_color=SECONDARY_TEXT)
        self.comp_size_label.grid(row=1, column=1, pady=(0, 5))

        self.savings_label = ctk.CTkLabel(self.info_card, text="Savings: -", font=ctk.CTkFont(size=14, weight="bold"), text_color=ACCENT_COLOR)
        self.savings_label.grid(row=2, column=0, columnspan=2, pady=(0, 15))

        # Output Card
        self.output_card = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.output_card.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.output_card.grid_columnconfigure(0, weight=1)

        self.dest_btn = ctk.CTkButton(self.output_card, text="📂 Choose Save Folder", command=self.select_output_folder, 
                                     fg_color="transparent", border_width=1, border_color="#475569", 
                                     hover_color="#1E293B", text_color=TEXT_COLOR)
        self.dest_btn.grid(row=0, column=0, pady=5)

        self.dest_label = ctk.CTkLabel(self.output_card, text="Save to: Not selected", 
                                      font=ctk.CTkFont(size=11), text_color=SECONDARY_TEXT)
        self.dest_label.grid(row=1, column=0)

        # Progress and Action
        self.progress_bar = ctk.CTkProgressBar(self.main_container, height=12, progress_color=ACCENT_COLOR)
        self.progress_bar.grid(row=3, column=0, sticky="ew", pady=(10, 20))
        self.progress_bar.set(0)

        self.compress_btn = ctk.CTkButton(self.main_container, text="⚡ COMPRESS NOW", 
                                         font=ctk.CTkFont(size=18, weight="bold"), height=60, 
                                         command=self.start_compression, fg_color=ACCENT_COLOR, 
                                         hover_color="#4F46E5")
        self.compress_btn.grid(row=4, column=0, sticky="ew", pady=(0, 20))

    def update_quality_label(self, value):
        self.quality_label.configure(text=f"Quality: {int(value)}%")

    def update_resize_label(self, value):
        self.resize_label.configure(text=f"Scale: {int(value)}%")

    def format_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def select_file(self):
        filetypes = (
            ('Media files', '*.jpg *.jpeg *.png *.mp4 *.mkv *.avi *.mov'),
            ('Images', '*.jpg *.jpeg *.png'),
            ('Videos', '*.mp4 *.mkv *.avi *.mov'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(title='Select a file', filetypes=filetypes)
        if filename:
            self.selected_file = filename
            self.file_label.configure(text=os.path.basename(filename))
            size = os.path.getsize(filename)
            self.orig_size_label.configure(text=f"Original Size: {self.format_size(size)}")
            self.comp_size_label.configure(text="Compressed Size: -", text_color=SECONDARY_TEXT)
            self.savings_label.configure(text="Savings: -", text_color=ACCENT_COLOR)
            
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png']:
                self.file_type = "image"
            else:
                self.file_type = "video"

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.dest_label.configure(text=f"Save to: {self.output_folder}")

    def start_compression(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        if not self.output_folder:
            messagebox.showwarning("Warning", "Please select an output folder!")
            return
        
        if self.is_compressing:
            return

        self.is_compressing = True
        self.compress_btn.configure(state="disabled", text="Compressing...")
        self.progress_bar.set(0)
        self.progress_bar.start()

        thread = threading.Thread(target=self.compress_task)
        thread.daemon = True
        thread.start()

    def compress_task(self):
        try:
            input_path = self.selected_file
            filename = os.path.basename(input_path)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(self.output_folder, f"{name}_compressed{ext}")

            if self.file_type == "image":
                self.compress_image(input_path, output_path)
            else:
                self.compress_video(input_path, output_path)

            final_size = os.path.getsize(output_path)
            
            self.after(0, lambda: self.compression_done(output_path, final_size))
        except Exception as e:
            self.after(0, lambda: self.compression_failed(str(e)))

    def compress_image(self, input_path, output_path):
        quality = int(self.quality_slider.get())
        scale = self.resize_slider.get() / 100.0

        img = Image.open(input_path)
        
        # Convert to RGB if necessary (for JPEG)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        if scale < 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        img.save(output_path, optimize=True, quality=quality)

    def compress_video(self, input_path, output_path):
        # Check if ffmpeg is available
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("FFmpeg not found. Please install FFmpeg to compress videos.")

        quality_preset = self.vid_quality_var.get()
        # CRF values: 18 (visually lossless) to 28 (default) to 51 (lowest)
        crf = "28"
        if quality_preset == "Low": crf = "32"
        elif quality_preset == "High": crf = "23"

        # Using libx264 for compatibility
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-vcodec", "libx264", "-crf", crf,
            "-acodec", "aac", "-strict", "experimental",
            output_path
        ]
        
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode != 0:
            error_msg = process.stderr.decode()
            raise Exception(f"FFmpeg Error: {error_msg}")

    def compression_done(self, output_path, final_size):
        self.progress_bar.stop()
        self.progress_bar.set(1)
        self.is_compressing = False
        self.compress_btn.configure(state="normal", text="⚡ COMPRESS NOW")
        
        orig_size = os.path.getsize(self.selected_file)
        savings = 0
        if orig_size > 0:
            savings = max(0, (1 - (final_size / orig_size)) * 100)
            
        self.comp_size_label.configure(text=f"Compressed Size: {self.format_size(final_size)}", text_color=SUCCESS_COLOR)
        self.savings_label.configure(text=f"Savings: {savings:.1f}% Reduction ✨", text_color=SUCCESS_COLOR)
        
        messagebox.showinfo("Success", f"Compression complete!\nSaved to: {output_path}\nSaved {savings:.1f}% space!")

    def compression_failed(self, error):
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.is_compressing = False
        self.compress_btn.configure(state="normal", text="⚡ COMPRESS NOW")
        messagebox.showerror("Error", f"Compression failed: {error}")

if __name__ == "__main__":
    app = MediaCompressorApp()
    app.mainloop()
