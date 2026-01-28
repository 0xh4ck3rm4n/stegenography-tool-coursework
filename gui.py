import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import img_operation as img_ops
import encode as encode
import decode as decode

# TODO: Steganography GUI
class SteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("600x500")
        
        self.image_path = None
        self.loaded_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        title_label = tk.Label(
            self.root, 
            text="Image Steganography Tool",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Image selection frame
        img_frame = tk.Frame(self.root)
        img_frame.pack(pady=10)
        
        self.img_label = tk.Label(img_frame, text="No image selected")
        self.img_label.pack(side=tk.LEFT, padx=5)
        
        select_btn = tk.Button(
            img_frame,
            text="Select Image",
            command=self.select_image
        )
        select_btn.pack(side=tk.LEFT, padx=5)
        
        # Encode section
        encode_frame = tk.LabelFrame(
            self.root,
            text="Encode Message",
            padx=10,
            pady=10
        )
        encode_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(encode_frame, text="Enter message to hide:").pack(anchor=tk.W)
        
        self.message_text = scrolledtext.ScrolledText(
            encode_frame,
            height=6,
            width=60
        )
        self.message_text.pack(pady=5)
        
        encode_btn = tk.Button(
            encode_frame,
            text="Encode & Save",
            command=self.encode_message,
            bg="#4CAF50",
            fg="white"
        )
        encode_btn.pack(pady=5)
        
        # Decode section
        decode_frame = tk.LabelFrame(
            self.root,
            text="Decode Message",
            padx=10,
            pady=10
        )
        decode_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        decode_btn = tk.Button(
            decode_frame,
            text="Decode Message",
            command=self.decode_message,
            bg="#2196F3",
            fg="white"
        )
        decode_btn.pack(pady=5)
        
        self.decoded_text = scrolledtext.ScrolledText(
            decode_frame,
            height=6,
            width=60,
            state=tk.DISABLED
        )
        self.decoded_text.pack(pady=5)
        
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
            
        if file_path:
            img = img_ops.load_image(file_path)
                
            if img and img_ops.validate_image(img):
                self.image_path = file_path
                self.loaded_image = img
                    
                # Update label
                filename = file_path.split('/')[-1]
                self.img_label.config(text=f"Selected: {filename}")
                    
                # Show capacityå
                capacity = encode.calculate_capacity(img.size)
                messagebox.showinfo(
                    "Image Loaded",
                    f"Image loaded successfully!\nMax capacity: {capacity} characters"
                )
            else:
                messagebox.showerror(
                    "Error",
                    "Invalid image. Please select an RGB image."
                )

    def encode_message(self):
        if not self.loaded_image:
            messagebox.showerror("Error", "Please select an image first!")
            return
        
        message = self.message_text.get("1.0", tk.END).strip()
        
        if not message:
            messagebox.showerror("Error", "Please enter a message to encode!")
            return
        
        # Get pixels
        pixels = img_ops.get_pixel_data(self.loaded_image)
        
        # Encode message
        new_pixels = encode.encode_message(pixels, message)
        
        if new_pixels is None:
            messagebox.showerror(
                "Error",
                "Message is too large for this image!"
            )
            return
        
        # Create new image
        new_img = img_ops.create_image_from_pixels(
            new_pixels,
            self.loaded_image.size
        )
        
        # Save image
        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        
        if output_path:
            if img_ops.save_image(new_img, output_path):
                messagebox.showinfo(
                    "Success",
                    "Message encoded and saved successfully!"
                )
                self.message_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Failed to save image!")

def create_gui():
        root = tk.Tk()
        # TODO: Steganography GUI 
        return root