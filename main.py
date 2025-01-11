import tkinter as tk
from processing.image_viewer import ImageViewer
from processing.image_processing import ImageProcessing

def main():
    root = tk.Tk()
    root.title("Image Viewer with OpenCV Functions")
    root.geometry("1000x700")
    root.configure(bg="#282c34")  # Darker background

    right_frame = tk.Frame(root, bg="#4A4E69")
    right_frame.grid(row=0, column=1, sticky="nsew")
    image_label = tk.Label(right_frame, bg="#4A4E69")
    image_label.pack(fill="both", expand=True)

    left_frame = tk.Frame(root, width=270, bg="#3e4451")
    left_frame.grid(row=0, column=0, sticky="ns")

    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    image_viewer = ImageViewer(root, image_label, left_frame)
    image_processing = ImageProcessing(image_viewer)
    image_viewer.image_processing = image_processing

    open_button = tk.Button(left_frame, text="Open Image", command=image_viewer.open_image, bg="#61afef", fg="white", font=("Arial", 12, "bold"), bd=0, highlightthickness=0)
    open_button.pack(pady=(20, 10), padx=10, fill="x") #Increased padding

    root.bind("<Configure>", lambda event: image_viewer.update_fonts())

    root.mainloop()

if __name__ == "__main__":
    main()