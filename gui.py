import tkinter as tk
import img_operation as img_ops
import encode as encode
import decode as decode

# TODO: Steganography GUI
class SteganographyGUI:
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("600x500")
        
        self.image_path = None
        self.loaded_image = None
        
        self.setup_ui()
        
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

def create_gui():
        root = tk.Tk()
        # TODO: Steganography GUI 
        return root