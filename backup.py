import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

def open_image():
    global cv_image, current_image, original_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if file_path:
        cv_image = cv2.imread(file_path)
        current_image = cv_image.copy()
        original_image = cv_image.copy()  # Save the original image for reverting
        show_image(cv_image)

def show_image(cv_img):
    img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    img_size = min(window_width // 2, window_height - 50)  # Adjust image size dynamically
    img = Image.fromarray(img)
    img = img.resize((img_size, img_size), Image.ANTIALIAS)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

def deselect_other_colors(selected_var):
    if selected_var != hsv_var:
        hsv_var.set(False)
    if selected_var != lab_var:
        lab_var.set(False)
    if selected_var != grayscale_var:
        grayscale_var.set(False)

def update_color():
    global current_image
    if cv_image is None:
        return

    current_image = cv_image.copy()

    # Apply color space conversions based on checkboxes
    if hsv_var.get():
        deselect_other_colors(hsv_var)
        current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2HSV)
    elif lab_var.get():
        deselect_other_colors(lab_var)
        current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2Lab)
    elif grayscale_var.get():
        deselect_other_colors(grayscale_var)
        current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        current_image = cv2.cvtColor(current_image, cv2.COLOR_GRAY2BGR)  # Convert back to 3-channel for display

    show_image(current_image)

def update_threshold():
    global current_image
    if cv_image is None:
        return

    # Ensure the image is grayscale before applying thresholding
    if not grayscale_var.get():
        current_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        grayscale_var.set(True)
        update_color()

    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    thresh_value = threshold_value.get()
    max_value = max_value_slider.get()

    if binary_var.get():
        _, current_image = cv2.threshold(gray_image, thresh_value, max_value, cv2.THRESH_BINARY)
    elif binary_inv_var.get():
        _, current_image = cv2.threshold(gray_image, thresh_value, max_value, cv2.THRESH_BINARY_INV)
    elif trunc_var.get():
        _, current_image = cv2.threshold(gray_image, thresh_value, max_value, cv2.THRESH_TRUNC)
    elif tozero_var.get():
        _, current_image = cv2.threshold(gray_image, thresh_value, max_value, cv2.THRESH_TOZERO)
    elif tozero_inv_var.get():
        _, current_image = cv2.threshold(gray_image, thresh_value, max_value, cv2.THRESH_TOZERO_INV)

    # Check if the current image is single-channel before converting
    if len(current_image.shape) == 2:  # Grayscale
        current_image = cv2.cvtColor(current_image, cv2.COLOR_GRAY2BGR)

    show_image(current_image)

def revert_to_original():
    global current_image
    if cv_image is None:
        return

    # Revert to the original image
    current_image = original_image.copy()
    show_image(current_image)

def toggle_threshold(checkbox_var):
    if not checkbox_var.get():
        revert_to_original()

def show_color_menu():
    color_frame.pack(fill="x", pady=5)
    threshold_frame.pack_forget()
    edge_frame.pack_forget()
    filter_frame.pack_forget()

def show_threshold_menu():
    if cv_image is not None and not grayscale_var.get():
        current_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        grayscale_var.set(True)
        update_color()

    threshold_frame.pack(fill="x", pady=5)
    color_frame.pack_forget()
    edge_frame.pack_forget()
    filter_frame.pack_forget()

def show_edge_menu():
    edge_frame.pack(fill="x", pady=5)
    color_frame.pack_forget()
    threshold_frame.pack_forget()
    filter_frame.pack_forget()

def show_filter_menu():
    filter_frame.pack(fill="x", pady=5)
    color_frame.pack_forget()
    threshold_frame.pack_forget()
    edge_frame.pack_forget()

def deselect_other_edge_methods(selected_var):
    if selected_var != sobel_var:
        sobel_var.set(False)
    if selected_var != canny_var:
        canny_var.set(False)

def update_edge_detection(*args):
    global current_image
    if cv_image is None:
        return

    current_image = cv_image.copy()

    if sobel_var.get():
        deselect_other_edge_methods(sobel_var)
        # Ensure the Sobel kernel size is odd and between 1 and 31
        sobel_kernel_size = sobel_kernel_slider.get()
        sobel_kernel_size = sobel_kernel_size if sobel_kernel_size % 2 == 1 else sobel_kernel_size + 1
        current_image = cv2.Sobel(current_image, cv2.CV_64F, 1, 0, ksize=sobel_kernel_size)
        current_image = cv2.convertScaleAbs(current_image)
    elif canny_var.get():
        deselect_other_edge_methods(canny_var)
        canny_low_threshold = canny_low_threshold_slider.get()
        canny_high_threshold = canny_high_threshold_slider.get()
        current_image = cv2.Canny(current_image, canny_low_threshold, canny_high_threshold)
        current_image = cv2.cvtColor(current_image, cv2.COLOR_GRAY2BGR)  # Convert to 3-channel for display

    show_image(current_image)

def apply_filter(selected_filter):
    global current_image
    if cv_image is None:
        return

    current_image = cv_image.copy()

    if selected_filter == "Blur":
        current_image = cv2.GaussianBlur(current_image, (5, 5), 0)
    elif selected_filter == "Sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        current_image = cv2.filter2D(current_image, -1, kernel)
    elif selected_filter == "Emboss":
        kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
        current_image = cv2.filter2D(current_image, -1, kernel)
    elif selected_filter == "Edge Enhance":
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        current_image = cv2.filter2D(current_image, -1, kernel)

    show_image(current_image)

def update_fonts():
    font_size = max(10, root.winfo_width() // 100)  # Adjust font size dynamically
    for widget in left_frame.winfo_children():
        widget.config(font=("Arial", font_size))

# Create the main window
root = tk.Tk()
root.title("Image Viewer with OpenCV Functions")
root.geometry("800x500")
root.configure(bg="#4A4E69")

# Bind resize event
root.bind("<Configure>", lambda event: [update_fonts(), show_image(current_image) if current_image is not None else None])

# Create the left frame
left_frame = tk.Frame(root, width=200, height=450, bg="#4A4E69")
left_frame.grid(row=0, column=0, sticky="nswe")

# Add a button to the top of the left frame
open_button = tk.Button(left_frame, text="Open Image", command=open_image, bg="#22223B", fg="white", font=("Arial", 12, "bold"))
open_button.pack(pady=10, padx=5, fill="x")

# Create a list menu
menu_frame = tk.Frame(left_frame, bg="#4A4E69")
menu_frame.pack(fill="x", pady=5)

color_button = tk.Button(menu_frame, text="Color", command=show_color_menu, bg="#22223B", fg="white", font=("Arial", 10))
color_button.pack(fill="x", pady=2, padx=5)

threshold_button = tk.Button(menu_frame, text="Thresholding", command=show_threshold_menu, bg="#22223B", fg="white", font=("Arial", 10))
threshold_button.pack(fill="x", pady=2, padx=5)

edge_button = tk.Button(menu_frame, text="Edge Detection", command=show_edge_menu, bg="#22223B", fg="white", font=("Arial", 10))
edge_button.pack(fill="x", pady=2, padx=5)

filter_button = tk.Button(menu_frame, text="Image Filtering", command=show_filter_menu, bg="#22223B", fg="white", font=("Arial", 10))
filter_button.pack(fill="x", pady=2, padx=5)

# Create color checkboxes
color_frame = tk.Frame(left_frame, bg="#8D99AE")
hsv_var = tk.BooleanVar()
lab_var = tk.BooleanVar()
grayscale_var = tk.BooleanVar()

hsv_checkbox = tk.Checkbutton(color_frame, text="HSV", variable=hsv_var, command=update_color, bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
hsv_checkbox.pack(anchor="w", padx=10, pady=2)

lab_checkbox = tk.Checkbutton(color_frame, text="L*a*b*", variable=lab_var, command=update_color, bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
lab_checkbox.pack(anchor="w", padx=10, pady=2)

grayscale_checkbox = tk.Checkbutton(color_frame, text="Grayscale", variable=grayscale_var, command=update_color, bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
grayscale_checkbox.pack(anchor="w", padx=10, pady=2)

# Create thresholding checkboxes and sliders
threshold_frame = tk.Frame(left_frame, bg="#8D99AE")
threshold_value = tk.IntVar(value=127)
max_value_slider = tk.IntVar(value=255)

binary_var = tk.BooleanVar()
binary_inv_var = tk.BooleanVar()
trunc_var = tk.BooleanVar()
tozero_var = tk.BooleanVar()
tozero_inv_var = tk.BooleanVar()

binary_checkbox = tk.Checkbutton(threshold_frame, text="THRESH_BINARY", variable=binary_var, command=lambda: [update_threshold() if binary_var.get() else toggle_threshold(binary_var)], bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
binary_checkbox.pack(anchor="w", padx=10, pady=2)

binary_inv_checkbox = tk.Checkbutton(threshold_frame, text="THRESH_BINARY_INV", variable=binary_inv_var, command=lambda: [update_threshold() if binary_inv_var.get() else toggle_threshold(binary_inv_var)], bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
binary_inv_checkbox.pack(anchor="w", padx=10, pady=2)

trunc_checkbox = tk.Checkbutton(threshold_frame, text="THRESH_TRUNC", variable=trunc_var, command=lambda: [update_threshold() if trunc_var.get() else toggle_threshold(trunc_var)], bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
trunc_checkbox.pack(anchor="w", padx=10, pady=2)

tozero_checkbox = tk.Checkbutton(threshold_frame, text="THRESH_TOZERO", variable=tozero_var, command=lambda: [update_threshold() if tozero_var.get() else toggle_threshold(tozero_var)], bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
tozero_checkbox.pack(anchor="w", padx=10, pady=2)

tozero_inv_checkbox = tk.Checkbutton(threshold_frame, text="THRESH_TOZERO_INV", variable=tozero_inv_var, command=lambda: [update_threshold() if tozero_inv_var.get() else toggle_threshold(tozero_inv_var)], bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
tozero_inv_checkbox.pack(anchor="w", padx=10, pady=2)

threshold_slider_label = tk.Label(threshold_frame, text="Threshold Value:", bg="#8D99AE", fg="white", font=("Arial", 10))
threshold_slider_label.pack(anchor="w", padx=10, pady=2)

threshold_slider = tk.Scale(threshold_frame, from_=0, to=255, variable=threshold_value, orient="horizontal", bg="#4A4E69", fg="white", length=150, command=lambda _: update_threshold())
threshold_slider.pack(anchor="w", padx=10, pady=2)

max_value_label = tk.Label(threshold_frame, text="Max Value:", bg="#8D99AE", fg="white", font=("Arial", 10))
max_value_label.pack(anchor="w", padx=10, pady=2)

max_value_scale = tk.Scale(threshold_frame, from_=0, to=255, variable=max_value_slider, orient="horizontal", bg="#4A4E69", fg="white", length=150, command=lambda _: update_threshold())
max_value_scale.pack(anchor="w", padx=10, pady=2)

# Create edge detection checkboxes and sliders
edge_frame = tk.Frame(left_frame, bg="#8D99AE")
sobel_var = tk.BooleanVar()
canny_var = tk.BooleanVar()

sobel_checkbox = tk.Checkbutton(edge_frame, text="Sobel", variable=sobel_var, command=lambda: update_edge_detection(), bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
sobel_checkbox.pack(anchor="w", padx=10, pady=2)

canny_checkbox = tk.Checkbutton(edge_frame, text="Canny", variable=canny_var, command=lambda: update_edge_detection(), bg="#8D99AE", fg="white", font=("Arial", 10), selectcolor="#4A4E69")
canny_checkbox.pack(anchor="w", padx=10, pady=2)

sobel_kernel_label = tk.Label(edge_frame, text="Sobel Kernel Size:", bg="#8D99AE", fg="white", font=("Arial", 10))
sobel_kernel_label.pack(anchor="w", padx=10, pady=2)

sobel_kernel_slider = tk.Scale(edge_frame, from_=1, to=31, orient="horizontal", bg="#4A4E69", fg="white", length=150, command=lambda _: update_edge_detection())
sobel_kernel_slider.pack(anchor="w", padx=10, pady=2)

canny_low_label = tk.Label(edge_frame, text="Canny Low Threshold:", bg="#8D99AE", fg="white", font=("Arial", 10))
canny_low_label.pack(anchor="w", padx=10, pady=2)

canny_low_threshold_slider = tk.Scale(edge_frame, from_=0, to=255, orient="horizontal", bg="#4A4E69", fg="white", length=150, command=lambda _: update_edge_detection())
canny_low_threshold_slider.pack(anchor="w", padx=10, pady=2)

canny_high_label = tk.Label(edge_frame, text="Canny High Threshold:", bg="#8D99AE", fg="white", font=("Arial", 10))
canny_high_label.pack(anchor="w", padx=10, pady=2)

canny_high_threshold_slider = tk.Scale(edge_frame, from_=0, to=255, orient="horizontal", bg="#4A4E69", fg="white", length=150, command=lambda _: update_edge_detection())
canny_high_threshold_slider.pack(anchor="w", padx=10, pady=2)

# Create filter buttons
filter_frame = tk.Frame(left_frame, bg="#8D99AE")
filter_buttons = ["Blur", "Sharpen", "Emboss", "Edge Enhance"]

for filter_name in filter_buttons:
    filter_button = tk.Button(filter_frame, text=filter_name, command=lambda f=filter_name: apply_filter(f), bg="#22223B", fg="white", font=("Arial", 10))
    filter_button.pack(fill="x", pady=2, padx=5)

# Create the right frame for the image display
right_frame = tk.Frame(root, bg="#4A4E69")
right_frame.grid(row=0, column=1, sticky="nswe")

image_label = tk.Label(right_frame, bg="#4A4E69")
image_label.pack(fill="both", expand=True)

# Configure resizing behavior
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Initialize global variables
cv_image = None
current_image = None
original_image = None

# Start the main loop
root.mainloop()