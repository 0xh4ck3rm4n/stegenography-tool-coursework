import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import img_operation as img_ops
import encode as encode
import decode as decode


class SteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography")
        self.root.geometry("720x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f17")

        self.bg          = "#0f0f17"
        self.card_bg     = "#161b22"
        self.text        = "#e6edf3"
        self.text_mute   = "#8b949e"
        self.accent      = "#58a6ff"
        self.accent_dark = "#388bfd"
        self.success     = "#3fb950"
        self.border      = "#30363d"

        self.image_path = None
        self.loaded_image = None

        self.setup_ui()

    def setup_ui(self):
        main = tk.Frame(self.root, bg=self.bg, padx=40, pady=32)
        main.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            main,
            text="Steganography",
            font=("Helvetica", 28, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(anchor="w")

        tk.Label(
            main,
            text="Hide messages inside images — simply & securely",
            font=("Helvetica", 11),
            bg=self.bg,
            fg=self.text_mute
        ).pack(anchor="w", pady=(4, 24))

        img_frame = tk.Frame(
            main,
            bg=self.card_bg,
            bd=1,
            relief="solid",
            highlightbackground=self.border,
            highlightthickness=1
        )
        img_frame.pack(fill=tk.X, pady=(0, 24), ipady=20)

        inner = tk.Frame(img_frame, bg=self.card_bg)
        inner.pack(padx=24, pady=16, fill=tk.X)

        self.img_status = tk.Label(
            inner,
            text="No image selected",
            font=("Helvetica", 11),
            bg=self.card_bg,
            fg=self.text_mute,
            anchor="w"
        )
        self.img_status.pack(side=tk.LEFT)

        self.select_btn = tk.Button(
            inner,
            text="Select Image",
            command=self.select_image,
            font=("Helvetica", 10, "bold"),
            bg=self.accent,
            fg="#000000",
            activebackground=self.accent_dark,
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            highlightthickness=0
        )
        self.select_btn.pack(side=tk.RIGHT)

        self.select_btn.bind("<Enter>", lambda e: self.select_btn.config(bg=self.accent_dark))
        self.select_btn.bind("<Leave>", lambda e: self.select_btn.config(bg=self.accent))

        encode_frame = tk.LabelFrame(
            main,
            text=" Encode Message ",
            padx=20,
            pady=20,
            bg=self.card_bg,
            fg=self.accent,
            font=("Helvetica", 12, "bold"),
            bd=1,
            relief="solid",
            highlightbackground=self.border,
            highlightthickness=1,
            labelanchor="n"
        )
        encode_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        tk.Label(
            encode_frame,
            text="Secret message",
            font=("Helvetica", 10),
            bg=self.card_bg,
            fg=self.text_mute,
            anchor="w"
        ).pack(anchor="w", pady=(0, 6))

        self.msg_entry = scrolledtext.ScrolledText(
            encode_frame,
            height=6,
            font=("Consolas", 11),
            bg="#0d1117",
            fg=self.text,
            insertbackground=self.accent,
            relief="flat",
            bd=0,
            padx=12,
            pady=10,
            wrap=tk.WORD
        )
        self.msg_entry.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        encode_btn = tk.Button(
            encode_frame,
            text="Encode & Save Image",
            command=self.encode_message,
            font=("Helvetica", 11, "bold"),
            bg=self.success,
            fg="#000000",
            activebackground="#2ea043",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            padx=32,
            pady=12,
            cursor="hand2"
        )
        encode_btn.pack(pady=8)

        encode_btn.bind("<Enter>", lambda e: encode_btn.config(bg="#2ea043"))
        encode_btn.bind("<Leave>", lambda e: encode_btn.config(bg=self.success))

        decode_frame = tk.LabelFrame(
            main,
            text=" Decode Message ",
            padx=20,
            pady=20,
            bg=self.card_bg,
            fg=self.accent,
            font=("Helvetica", 12, "bold"),
            bd=1,
            relief="solid",
            highlightbackground=self.border,
            highlightthickness=1,
            labelanchor="n"
        )
        decode_frame.pack(fill=tk.BOTH, expand=True)

        decode_btn = tk.Button(
            decode_frame,
            text="Extract Hidden Message",
            command=self.decode_message,
            font=("Helvetica", 11, "bold"),
            bg=self.accent,
            fg="#000000",
            activebackground=self.accent_dark,
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            padx=32,
            pady=12,
            cursor="hand2"
        )
        decode_btn.pack(pady=(8, 16))

        decode_btn.bind("<Enter>", lambda e: decode_btn.config(bg=self.accent_dark))
        decode_btn.bind("<Leave>", lambda e: decode_btn.config(bg=self.accent))

        self.result_text = scrolledtext.ScrolledText(
            decode_frame,
            height=6,
            font=("Consolas", 11),
            state="disabled",
            bg="#0d1117",
            fg=self.text,
            relief="flat",
            bd=0,
            padx=12,
            pady=10
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def select_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        if not path:
            return

        img = img_ops.load_image(path)
        if not img or not img_ops.validate_image(img):
            messagebox.showerror("Error", "Please select a valid RGB image.")
            return

        self.image_path = path
        self.loaded_image = img

        name = path.split("/")[-1]
        if len(name) > 28:
            name = name[:25] + "…"

        self.img_status.config(
            text=f"✓  {name}",
            fg=self.success,
            font=("Helvetica", 11, "bold")
        )

        cap = encode.calculate_capacity(img.size)
        messagebox.showinfo("Image Loaded", f"Capacity: ≈ {cap:,} characters")

    def encode_message(self):
        if not self.loaded_image:
            messagebox.showerror("Error", "No image selected.")
            return

        msg = self.msg_entry.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("Warning", "Please enter a message.")
            return

        pixels = img_ops.get_pixel_data(self.loaded_image)
        new_pixels = encode.encode_message(pixels, msg)

        if new_pixels is None:
            messagebox.showerror("Error", "Message too long for this image.")
            return

        new_img = img_ops.create_image_from_pixels(new_pixels, self.loaded_image.size)

        out_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
            title="Save encoded image"
        )
        if not out_path:
            return

        if img_ops.save_image(new_img, out_path):
            messagebox.showinfo("Success", "Image saved successfully.")
            self.msg_entry.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Could not save the image.")

    def decode_message(self):
        if not self.loaded_image:
            messagebox.showerror("Error", "No image selected.")
            return

        pixels = img_ops.get_pixel_data(self.loaded_image)
        message = decode.decode_message(pixels)

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        if message:
            self.result_text.insert("1.0", message)
            messagebox.showinfo("Success", "Message extracted.")
        else:
            self.result_text.insert("1.0", "(no hidden message found)")
            messagebox.showinfo("Result", "No message found in this image.")

        self.result_text.config(state="disabled")

def create_gui():
    root = tk.Tk()
    SteganographyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    create_gui()