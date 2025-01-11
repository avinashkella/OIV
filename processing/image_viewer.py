import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2

class ImageViewer:
    def __init__(self, root, image_label, left_frame):
        self.root = root
        self.image_label = image_label
        self.left_frame = left_frame
        self.cv_image = None
        self.current_image = None
        self.original_image = None
        self.image_processing = None
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=6, font=("Arial", 10), background="#4c566a", foreground="white", borderwidth=0, highlightthickness=0) #Modified Buttons
        self.style.configure("TCheckbutton", font=("Arial", 10), background="#4c566a", foreground="white") #Modified Checkbuttons
        self.style.configure("TScale", background="#4c566a", foreground="white") #Modified Scales
        self.style.configure("TLabel", background="#4c566a", foreground="white", font=("Arial", 10)) #Modified Labels
        self.style.configure("Menu.TFrame", background="#3e4451") #Modified Menu Frame
        self.create_menu()
        self.current_frame = None

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            self.cv_image = cv2.imread(file_path)
            if self.cv_image is None:
                print("Error: Could not open image. Check file path and format.")
                return
            self.current_image = self.cv_image.copy()
            self.original_image = self.cv_image.copy()
            self.show_image(self.current_image)
            self.update_fonts()

    def show_image(self, cv_img):
        if cv_img is None:
            return
        img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        img_size = min(window_width // 2, window_height - 100)
        try:
            img = Image.fromarray(img)
            img = img.resize((img_size, img_size), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
        except Exception as e:
            print(f"Error displaying image: {e}")

    def update_fonts(self):
        font_size = max(10, self.root.winfo_width() // 80) #Adjust divisor for scaling
        font = ("Arial", font_size)  # Create font tuple ONCE

        # Update fonts for all relevant widgets in left_frame
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, (tk.Button, ttk.Button, ttk.Checkbutton, ttk.Label)): #Check widget types
                try:
                    widget.config(font=font)
                except tk.TclError as e:
                    print(f"Error setting font for {widget}: {e}")

    def create_menu(self):
        menu_frame = ttk.Frame(self.left_frame, style="Menu.TFrame")
        menu_frame.pack(fill="x", pady=(0, 15), padx=10) #Added padding between menu and submenus

        buttons = [
            ("Color", self.show_color_menu),
            ("Thresholding", self.show_threshold_menu),
            ("Edge Detection", self.show_edge_menu),
            ("Image Filtering", self.show_filter_menu),
            ("Revert to Original", self.revert_image)
        ]

        for text, command in buttons:
            ttk.Button(menu_frame, text=text, command=command).pack(fill="x", pady=5) #Increased padding between buttons

        self.color_frame = ttk.Frame(self.left_frame, style="Menu.TFrame", padding=(10,0)) #Added padding to submenus
        self.threshold_frame = ttk.Frame(self.left_frame, style="Menu.TFrame", padding=(10,0))
        self.edge_frame = ttk.Frame(self.left_frame, style="Menu.TFrame", padding=(10,0))
        self.filter_frame = ttk.Frame(self.left_frame, style="Menu.TFrame", padding=(10,0))

    def revert_image(self):
        if self.image_processing:
            self.image_processing.revert_to_original()

    def show_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
            for widget in self.current_frame.winfo_children():
                widget.destroy()
        frame.pack(fill="x", pady=(0, 10), padx=5)
        self.current_frame = frame

    def show_color_menu(self):
        self.show_frame(self.color_frame)
        self.image_processing.create_color_options(self.color_frame)

    def show_threshold_menu(self):
        self.show_frame(self.threshold_frame)
        self.image_processing.create_threshold_options(self.threshold_frame)

    def show_edge_menu(self):
        self.show_frame(self.edge_frame)
        self.image_processing.create_edge_options(self.edge_frame)

    def show_filter_menu(self):
        self.show_frame(self.filter_frame)
        self.image_processing.create_filter_options(self.filter_frame)