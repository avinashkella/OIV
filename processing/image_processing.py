import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

class ImageProcessing:
    def __init__(self, image_viewer):
        self.image_viewer = image_viewer
        self.last_color_conversion = None

    def update_image(self):
        self.image_viewer.show_image(self.image_viewer.current_image)

    def create_color_options(self, frame):
        hsv_var = tk.BooleanVar()
        lab_var = tk.BooleanVar()
        grayscale_var = tk.BooleanVar()

        def update_color():
            if self.image_viewer.cv_image is None:
                return

            self.image_viewer.current_image = self.image_viewer.cv_image.copy()  # Start with original

            if hsv_var.get():
                self.image_viewer.current_image = cv2.cvtColor(self.image_viewer.current_image, cv2.COLOR_BGR2HSV)
                self.last_color_conversion = "hsv"
            elif lab_var.get():
                self.image_viewer.current_image = cv2.cvtColor(self.image_viewer.current_image, cv2.COLOR_BGR2Lab)
                self.last_color_conversion = "lab"
            elif grayscale_var.get():
                self.image_viewer.current_image = cv2.cvtColor(self.image_viewer.current_image, cv2.COLOR_BGR2GRAY)
                self.image_viewer.current_image = cv2.cvtColor(self.image_viewer.current_image, cv2.COLOR_GRAY2BGR) #Convert back to BGR for display
                self.last_color_conversion = "grayscale"
            else:  # No conversion selected, revert to original
                if self.image_viewer.original_image is not None:
                    self.image_viewer.current_image = self.image_viewer.original_image.copy()
                self.last_color_conversion = None

            self.update_image()

        def on_checkbutton_click(var, other_vars): #Function to uncheck other buttons
            if var.get(): #If the clicked button is checked
                for other_var in other_vars:
                    other_var.set(False) #Uncheck the other buttons
            update_color() #Call update_color to apply changes

        ttk.Checkbutton(frame, text="HSV", variable=hsv_var, command=lambda: on_checkbutton_click(hsv_var, [lab_var, grayscale_var])).pack(anchor="w", padx=10, pady=3)
        ttk.Checkbutton(frame, text="Lab", variable=lab_var, command=lambda: on_checkbutton_click(lab_var, [hsv_var, grayscale_var])).pack(anchor="w", padx=10, pady=3)
        ttk.Checkbutton(frame, text="Grayscale", variable=grayscale_var, command=lambda: on_checkbutton_click(grayscale_var, [hsv_var, lab_var])).pack(anchor="w", padx=10, pady=3)


    def create_threshold_options(self, frame):
        thresh_var = tk.IntVar(value=127)
        max_val_var = tk.IntVar(value=255)
        binary_var = tk.BooleanVar()
        binary_inv_var = tk.BooleanVar()
        trunc_var = tk.BooleanVar()
        tozero_var = tk.BooleanVar()
        tozero_inv_var = tk.BooleanVar()

        def update_threshold():
            if self.image_viewer.cv_image is None:
                return
            gray = cv2.cvtColor(self.image_viewer.cv_image.copy(), cv2.COLOR_BGR2GRAY)
            thresh = thresh_var.get()
            max_val = max_val_var.get()

            if binary_var.get():
                _, self.image_viewer.current_image = cv2.threshold(gray, thresh, max_val, cv2.THRESH_BINARY)
            elif binary_inv_var.get():
                _, self.image_viewer.current_image = cv2.threshold(gray, thresh, max_val, cv2.THRESH_BINARY_INV)
            elif trunc_var.get():
                _, self.image_viewer.current_image = cv2.threshold(gray, thresh, max_val, cv2.THRESH_TRUNC)
            elif tozero_var.get():
                _, self.image_viewer.current_image = cv2.threshold(gray, thresh, max_val, cv2.THRESH_TOZERO)
            elif tozero_inv_var.get():
                _, self.image_viewer.current_image = cv2.threshold(gray, thresh, max_val, cv2.THRESH_TOZERO_INV)
            else:  # No threshold selected, revert to grayscale
                self.image_viewer.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR) #Convert to BGR for display

            self.update_image()

        def on_threshold_checkbutton_click(var, other_vars):
            if var.get():
                for other_var in other_vars:
                    other_var.set(False)
            update_threshold()

        ttk.Label(frame, text="Threshold Value:").pack(anchor="w", padx=10, pady=(5,2))
        ttk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=thresh_var, command=lambda x: update_threshold()).pack(fill="x", padx=10, pady=(0,5))
        ttk.Label(frame, text="Max Value:").pack(anchor="w", padx=10, pady=(5,2))
        ttk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=max_val_var, command=lambda x: update_threshold()).pack(fill="x", padx=10, pady=(0,5))

        ttk.Checkbutton(frame, text="Binary", variable=binary_var, command=lambda: on_threshold_checkbutton_click(binary_var, [binary_inv_var, trunc_var, tozero_var, tozero_inv_var])).pack(anchor="w", padx=10, pady=3)
        ttk.Checkbutton(frame, text="Binary Inverted", variable=binary_inv_var, command=lambda: on_threshold_checkbutton_click(binary_inv_var, [binary_var, trunc_var, tozero_var, tozero_inv_var])).pack(anchor="w", padx=10, pady=3)
        ttk.Checkbutton(frame, text="Truncate", variable=trunc_var, command=lambda: on_threshold_checkbutton_click(trunc_var, [binary_var, binary_inv_var, tozero_var, tozero_inv_var])).pack(anchor="w", padx=10, pady=3)
        ttk.Checkbutton(frame, text="To Zero", variable=tozero_var, command=lambda: on_threshold_checkbutton_click(tozero_var, [binary_var, binary_inv_var, trunc_var, tozero_inv_var])).pack(anchor="w", padx=10, pady=3)
        ttk.Checkbutton(frame, text="To Zero Inverted", variable=tozero_inv_var, command=lambda: on_threshold_checkbutton_click(tozero_inv_var, [binary_var, binary_inv_var, trunc_var, tozero_var])).pack(anchor="w", padx=10, pady=3)

    def revert_to_original(self):
        if self.image_viewer.original_image is None:
            return
        self.image_viewer.current_image = self.image_viewer.original_image.copy()
        self.update_image()

    def create_edge_options(self, frame):
        canny_var = tk.BooleanVar()
        sobel_var = tk.BooleanVar()

        canny_low = tk.IntVar(value=50)
        canny_high = tk.IntVar(value=150)

        sobel_dx = tk.IntVar(value=1)
        sobel_dy = tk.IntVar(value=0)
        sobel_ksize = tk.IntVar(value=3)

        def update_edges(event=None):
            if self.image_viewer.cv_image is None:
                return
            gray = cv2.cvtColor(self.image_viewer.cv_image.copy(), cv2.COLOR_BGR2GRAY)

            if canny_var.get():
                self.image_viewer.current_image = cv2.Canny(gray, canny_low.get(), canny_high.get())
            elif sobel_var.get():
                dx = sobel_dx.get()
                dy = sobel_dy.get()
                ksize = sobel_ksize.get()

                if ksize not in (1, 3, 5, 7):
                    ksize = 3

                # CRITICAL FIX: Handle dx=0 or dy=0 correctly
                if dx == 0 and dy == 0:
                    self.image_viewer.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR) #If both are zero then show gray image
                    self.update_image()
                    return #Exit early to avoid the error.
                elif dx==0:
                    sobel = cv2.Sobel(gray, cv2.CV_64F, dx, 1, ksize=ksize)
                elif dy==0:
                    sobel = cv2.Sobel(gray, cv2.CV_64F, 1, dy, ksize=ksize)
                else:
                    sobelx = cv2.Sobel(gray, cv2.CV_64F, dx, 0, ksize=ksize)
                    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, dy, ksize=ksize)
                    sobel = np.sqrt(sobelx**2 + sobely**2)

                sobel = np.uint8(sobel)
                self.image_viewer.current_image = sobel
            else:
                self.image_viewer.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            self.image_viewer.current_image = cv2.cvtColor(self.image_viewer.current_image, cv2.COLOR_GRAY2BGR)
            self.update_image()

        def on_edge_checkbutton_click(var, other_vars):
            if var.get():
                for other_var in other_vars:
                    other_var.set(False)
            update_edges()

        ttk.Checkbutton(frame, text="Canny", variable=canny_var, command=lambda: on_edge_checkbutton_click(canny_var, [sobel_var])).pack(anchor="w", padx=10, pady=3)
        ttk.Label(frame, text="Canny Low Threshold:").pack(anchor="w", padx=10, pady=(0, 0))
        ttk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=canny_low, command=update_edges).pack(fill="x", padx=10, pady=(0, 5))
        ttk.Label(frame, text="Canny High Threshold:").pack(anchor="w", padx=10, pady=(0, 10))
        ttk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=canny_high, command=update_edges).pack(fill="x", padx=10, pady=(0, 10))

        ttk.Checkbutton(frame, text="Sobel", variable=sobel_var, command=lambda: on_edge_checkbutton_click(sobel_var, [canny_var])).pack(anchor="w", padx=10, pady=3)
        ttk.Label(frame, text="Sobel dx:").pack(anchor="w", padx=10, pady=(0, 0))
        ttk.Scale(frame, from_=0, to=1, orient=tk.HORIZONTAL, variable=sobel_dx, command=update_edges).pack(fill="x", padx=10, pady=(0, 5))
        ttk.Label(frame, text="Sobel dy:").pack(anchor="w", padx=10, pady=(0, 0))
        ttk.Scale(frame, from_=0, to=1, orient=tk.HORIZONTAL, variable=sobel_dy, command=update_edges).pack(fill="x", padx=10, pady=(0, 5))
        ttk.Label(frame, text="Sobel Kernel Size:").pack(anchor="w", padx=10, pady=(0, 0))
        ttk.Scale(frame, from_=1, to=7, orient=tk.HORIZONTAL, variable=sobel_ksize, command=update_edges).pack(fill="x", padx=10, pady=(0, 10))

    def create_filter_options(self, frame):
        blur_kernel_var = tk.IntVar(value=3)  # Default kernel size
        sharpen_kernel_var = tk.IntVar(value=3)  # Default kernel size

        def apply_blur():
            if self.image_viewer.cv_image is None:
                return
            kernel_size = blur_kernel_var.get()
            if kernel_size % 2 == 0:  # Ensure kernel size is odd
                kernel_size += 1
            self.image_viewer.current_image = cv2.blur(self.image_viewer.cv_image.copy(), (kernel_size, kernel_size))
            self.update_image()

        def apply_sharpen():
            if self.image_viewer.cv_image is None:
                return
            kernel_size = sharpen_kernel_var.get()
            if kernel_size % 2 == 0:  # Ensure kernel size is odd
                kernel_size += 1
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            self.image_viewer.current_image = cv2.filter2D(self.image_viewer.cv_image.copy(), -1, kernel)
            self.update_image()

        ttk.Label(frame, text="Blur Kernel Size:").pack(anchor="w", padx=10, pady=(5,2))
        ttk.Scale(frame, from_=1, to=11, orient=tk.HORIZONTAL, variable=blur_kernel_var, command=lambda x: apply_blur()).pack(fill="x", padx=10, pady=(0,5))
        ttk.Label(frame, text="Sharpen Kernel Size:").pack(anchor="w", padx=10, pady=(5,2))
        ttk.Scale(frame, from_=1, to=11, orient=tk.HORIZONTAL, variable=sharpen_kernel_var, command=lambda x: apply_sharpen()).pack(fill="x", padx=10, pady=(0,5))  

    def create_sift_options(self, frame):
        sift_var = tk.BooleanVar()
        show_location_var = tk.BooleanVar()
        show_size_var = tk.BooleanVar()  # Represents scale/size
        show_orientation_var = tk.BooleanVar()

        def update_sift():
            if self.image_viewer.cv_image is None:
                return
            gray = cv2.cvtColor(self.image_viewer.cv_image.copy(), cv2.COLOR_BGR2GRAY)

            if sift_var.get():
                sift = cv2.xfeatures2d.SIFT_create()
                keypoints, descriptors = sift.detectAndCompute(gray, None)

                img_with_keypoints = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

                for kp in keypoints:
                    x, y = int(kp.pt[0]), int(kp.pt[1])
                    size = int(kp.size / 2)
                    angle = kp.angle

                    if show_location_var.get():
                        cv2.circle(img_with_keypoints, (x, y), 3, (0, 255, 0), -1)  # Increased radius to 3

                    if show_size_var.get():
                        cv2.circle(img_with_keypoints, (x, y), size, (0, 255, 0), 1)

                    if show_orientation_var.get():
                        end_x = int(x + size * np.cos(np.deg2rad(angle)))
                        end_y = int(y + size * np.sin(np.deg2rad(angle)))
                        cv2.line(img_with_keypoints, (x, y), (end_x, end_y), (0, 255, 0), 1)

                self.image_viewer.current_image = img_with_keypoints
            else:
                if self.image_viewer.original_image is not None:
                    self.image_viewer.current_image = self.image_viewer.original_image.copy()
                else:
                    self.image_viewer.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            self.update_image()

        ttk.Checkbutton(frame, text="Enable SIFT", variable=sift_var, command=update_sift).pack(anchor="w", padx=10, pady=3)
        ttk.Checkbutton(frame, text="Show Location", variable=show_location_var, command=update_sift).pack(anchor="w", padx=20, pady=2)
        ttk.Checkbutton(frame, text="Show Size", variable=show_size_var, command=update_sift).pack(anchor="w", padx=20, pady=2)
        ttk.Checkbutton(frame, text="Show Orientation", variable=show_orientation_var, command=update_sift).pack(anchor="w", padx=20, pady=2)

        
                                                            