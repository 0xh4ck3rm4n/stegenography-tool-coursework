
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import tkinter.simpledialog as simpledialog
from PIL import Image, ImageTk
import img_operation as img_ops
import encode as enc
import decode as dec
import crypto
import compression
import os
from pathlib import Path


class SteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography v2.0")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        self.root.configure(bg="#0f0f17")

        self.bg          = "#0f0f17"
        self.card_bg     = "#161b22"
        self.text        = "#e6edf3"
        self.text_mute   = "#8b949e"
        self.accent      = "#58a6ff"
        self.accent_dark = "#388bfd"
        self.success     = "#3fb950"
        self.error       = "#f85149"
        self.border      = "#30363d"
        self.warning     = "#f0883e"

        self.image_path = None
        self.loaded_image = None
        self.hide_mode = "text"

        self.setup_ui()
        self.setup_drag_drop()

    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10])

        self.encode_frame = tk.Frame(notebook, bg=self.bg)
        self.decode_frame = tk.Frame(notebook, bg=self.bg)
        self.info_frame = tk.Frame(notebook, bg=self.bg)

        notebook.add(self.encode_frame, text="  Encode  ")
        notebook.add(self.decode_frame, text="  Decode  ")
        notebook.add(self.info_frame, text="  Info  ")

        self.setup_encode_tab()
        self.setup_decode_tab()
        self.setup_info_tab()

    def setup_encode_tab(self):
        main = tk.Frame(self.encode_frame, bg=self.bg, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(
            main,
            text="Encode Message",
            font=("Helvetica", 18, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            main,
            text="Select an image, enter your message, and encode",
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text_mute
        ).pack(anchor="w", pady=(0, 18))

        # ===== Image Selection =====
        img_frame = tk.Frame(
            main,
            bg=self.card_bg,
            bd=1,
            relief="solid",
            highlightbackground=self.border,
            highlightthickness=1
        )
        img_frame.pack(fill=tk.X, pady=(0, 20), ipady=15)

        inner = tk.Frame(img_frame, bg=self.card_bg)
        inner.pack(padx=20, pady=12, fill=tk.X)

        self.img_status_enc = tk.Label(
            inner,
            text="No image selected",
            font=("Helvetica", 11),
            bg=self.card_bg,
            fg=self.text_mute,
            anchor="w"
        )
        self.img_status_enc.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            inner,
            text="Browse",
            command=self.select_image,
            font=("Helvetica", 10, "bold"),
            bg=self.accent,
            fg="#000000",
            activebackground=self.accent_dark,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            highlightthickness=0
        ).pack(side=tk.RIGHT)

        mode_frame = tk.Frame(main, bg=self.bg)
        mode_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            mode_frame,
            text="What to hide:",
            font=("Helvetica", 10, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(side=tk.LEFT, padx=(0, 15))

        self.hide_var = tk.StringVar(value="text")

        tk.Radiobutton(
            mode_frame,
            text="Text Message",
            variable=self.hide_var,
            value="text",
            command=self.update_hide_mode,
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT)

        tk.Radiobutton(
            mode_frame,
            text="File",
            variable=self.hide_var,
            value="file",
            command=self.update_hide_mode,
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT, padx=(30, 0))

        self.content_frame = tk.Frame(main, bg=self.bg)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.text_label = tk.Label(
            self.content_frame,
            text="Secret message",
            font=("Helvetica", 10, "bold"),
            bg=self.bg,
            fg=self.text_mute
        )
        self.text_label.pack(anchor="w", pady=(0, 8))

        self.msg_entry = scrolledtext.ScrolledText(
            self.content_frame,
            height=8,
            font=("Consolas", 10),
            bg="#0d1117",
            fg=self.text,
            insertbackground=self.accent,
            relief="flat",
            bd=0,
            padx=12,
            pady=10,
            wrap=tk.WORD
        )
        self.msg_entry.pack(fill=tk.BOTH, expand=True)

        self.file_label_text = tk.Label(
            self.content_frame,
            text="File to hide",
            font=("Helvetica", 10, "bold"),
            bg=self.bg,
            fg=self.text_mute
        )

        self.file_info_label = tk.Label(
            self.content_frame,
            text="(No file selected)",
            font=("Consolas", 10),
            bg="#0d1117",
            fg=self.text_mute
        )

        opts_frame = tk.Frame(main, bg=self.bg)
        opts_frame.pack(fill=tk.X, pady=15)

        self.compress_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            opts_frame,
            text="Compress before hiding",
            variable=self.compress_var,
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT)

        self.encrypt_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            opts_frame,
            text="Encrypt with password",
            variable=self.encrypt_var,
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT, padx=(40, 0))

        self.randomize_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            opts_frame,
            text="Randomize embedding",
            variable=self.randomize_var,
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT, padx=(40, 0))

        self.progress_enc = ttk.Progressbar(
            main,
            mode='indeterminate',
            length=300
        )
        self.progress_enc.pack(fill=tk.X, pady=(0, 12))

        tk.Button(
            main,
            text="Encode & Save Image",
            command=self.encode_message,
            font=("Helvetica", 11, "bold"),
            bg=self.success,
            fg="#000000",
            activebackground="#2ea043",
            relief="flat",
            bd=0,
            padx=32,
            pady=11,
            cursor="hand2"
        ).pack(fill=tk.X)

    def update_hide_mode(self):
        """Switch between text and file mode."""
        self.hide_mode = self.hide_var.get()

        if self.hide_mode == "file":
            self.text_label.config(text="File to hide")
            self.msg_entry.config(state=tk.DISABLED)
            self.file_label_text.pack(fill=tk.X, pady=(0, 8))
            self.file_info_label.pack(fill=tk.X, padx=12, pady=4)
        else:
            self.text_label.config(text="Secret message")
            self.msg_entry.config(state=tk.NORMAL)
            self.file_label_text.pack_forget()
            self.file_info_label.pack_forget()

    def setup_decode_tab(self):
        """Build the decoding interface."""
        main = tk.Frame(self.decode_frame, bg=self.bg, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(
            main,
            text="Decode Message",
            font=("Helvetica", 18, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            main,
            text="Select an encoded image to extract the hidden message",
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text_mute
        ).pack(anchor="w", pady=(0, 18))

        img_frame = tk.Frame(
            main,
            bg=self.card_bg,
            bd=1,
            relief="solid",
            highlightbackground=self.border,
            highlightthickness=1
        )
        img_frame.pack(fill=tk.X, pady=(0, 20), ipady=15)

        inner = tk.Frame(img_frame, bg=self.card_bg)
        inner.pack(padx=20, pady=12, fill=tk.X)

        self.img_status_dec = tk.Label(
            inner,
            text="No image selected",
            font=("Helvetica", 11),
            bg=self.card_bg,
            fg=self.text_mute,
            anchor="w"
        )
        self.img_status_dec.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            inner,
            text="Browse",
            command=self.select_image_for_decode,
            font=("Helvetica", 10, "bold"),
            bg=self.accent,
            fg="#000000",
            activebackground=self.accent_dark,
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            highlightthickness=0
        ).pack(side=tk.RIGHT)

        type_frame = tk.Frame(main, bg=self.bg)
        type_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            type_frame,
            text="Extract:",
            font=("Helvetica", 10, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(side=tk.LEFT, padx=(0, 15))

        self.extract_var = tk.StringVar(value="auto")

        tk.Radiobutton(
            type_frame,
            text="Auto-detect",
            variable=self.extract_var,
            value="auto",
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT)

        tk.Radiobutton(
            type_frame,
            text="Text Message",
            variable=self.extract_var,
            value="text",
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT, padx=(30, 0))

        tk.Radiobutton(
            type_frame,
            text="File",
            variable=self.extract_var,
            value="file",
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT, padx=(30, 0))

        # ===== Options =====
        opts_frame = tk.Frame(main, bg=self.bg)
        opts_frame.pack(fill=tk.X, pady=(0, 15))

        self.decrypt_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            opts_frame,
            text="🔓 Try decryption with password",
            variable=self.decrypt_var,
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT)

        self.use_seed_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            opts_frame,
            text="Use custom seed",
            variable=self.use_seed_var,
            font=("Helvetica", 10),
            bg=self.bg,
            fg=self.text,
            selectcolor=self.card_bg,
            activebackground=self.bg,
            activeforeground=self.accent
        ).pack(side=tk.LEFT, padx=(40, 0))

        self.progress_dec = ttk.Progressbar(
            main,
            mode='indeterminate',
            length=300
        )
        self.progress_dec.pack(fill=tk.X, pady=(0, 12))

        tk.Label(
            main,
            text="Extracted Content",
            font=("Helvetica", 10, "bold"),
            bg=self.bg,
            fg=self.text_mute
        ).pack(anchor="w", pady=(0, 8))

        result_frame = tk.Frame(
            main,
            bg=self.card_bg,
            bd=1,
            relief="solid",
            highlightbackground=self.border,
            highlightthickness=1
        )
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=10,
            font=("Consolas", 10),
            bg="#0d1117",
            fg=self.text,
            relief="flat",
            bd=0,
            padx=12,
            pady=10
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(main, bg=self.bg)
        btn_frame.pack(fill=tk.X)

        tk.Button(
            btn_frame,
            text="Extract Message",
            command=self.decode_message,
            font=("Helvetica", 11, "bold"),
            bg=self.accent,
            fg="#000000",
            activebackground=self.accent_dark,
            relief="flat",
            bd=0,
            padx=28,
            pady=10,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            btn_frame,
            text="Copy",
            command=self.copy_result,
            font=("Helvetica", 11, "bold"),
            bg=self.text_mute,
            fg="#000000",
            activebackground=self.text_mute,
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(side=tk.LEFT)

    def setup_info_tab(self):
        """Build the info/about interface."""
        main = tk.Frame(self.info_frame, bg=self.bg, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(
            main,
            text="About Steganography v2.0",
            font=("Helvetica", 20, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(anchor="w", pady=(0, 20))

        # Info text
        info_text = """
Welcome to Steganography Tool

Features:
  • Password-based AES Encryption (Fernet)
  • Hide text messages in images
  • Hide any file type (PDF, ZIP, images, etc.)
  • Optional compression (zlib)
  • Randomized pixel embedding (harder to detect)
  • Support for PNG, JPG, BMP images

Version: 2.0
License: MIT
Author: Gaurav Poudel
        """

        info_label = scrolledtext.ScrolledText(
            main,
            height=20,
            font=("Consolas", 9),
            bg="#0d1117",
            fg=self.text,
            relief="flat",
            bd=0,
            padx=12,
            pady=10
        )
        info_label.pack(fill=tk.BOTH, expand=True)
        info_label.insert("1.0", info_text.strip())
        info_label.config(state=tk.DISABLED)

    # ==================== HELPER METHODS ====================

    def select_image(self):
        """Select image for encoding."""
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        if not path:
            return

        img = img_ops.load_img(path)
        if not img or not img_ops.img_validation(img):
            messagebox.showerror("Error", "Please select a valid RGB image.")
            return

        self.image_path = path
        self.loaded_image = img

        name = Path(path).name
        if len(name) > 40:
            name = name[:37] + "…"

        cap = enc.calculate_capacity(img.size)
        self.img_status_enc.config(
            text=f"{name} (capacity: ~{cap:,} chars)",
            fg=self.success,
            font=("Helvetica", 10, "bold")
        )

    def select_image_for_decode(self):
        """Select image for decoding."""
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        if not path:
            return

        img = img_ops.load_img(path)
        if not img or not img_ops.img_validation(img):
            messagebox.showerror("Error", "Invalid image selected.")
            return

        self.image_path = path
        self.loaded_image = img

        name = Path(path).name
        if len(name) > 40:
            name = name[:37] + "…"

        self.img_status_dec.config(
            text=f"{name}",
            fg=self.success,
            font=("Helvetica", 10, "bold")
        )

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)

    def encode_message(self):
        """Encode message into image."""
        if not self.loaded_image:
            messagebox.showerror("Error", "No image selected.")
            return

        if self.hide_mode == "text":
            msg = self.msg_entry.get("1.0", tk.END).strip()
            if not msg:
                messagebox.showwarning("Warning", "Please enter a message.")
                return

            self.progress_enc.start()
            self.root.update()

            # Get options
            compress = self.compress_var.get()
            encrypt = self.encrypt_var.get()
            randomize = self.randomize_var.get()

            password = None
            seed = None
            data_to_hide = msg

            # Handle encryption
            if encrypt:
                password = simpledialog.askstring(
                    "Encryption",
                    "Enter password (leave blank for no encryption):",
                    show="*"
                )
                if password is None:
                    self.progress_enc.stop()
                    return

                if password:
                    data_to_hide = crypto.encrypt_message(msg, password)

            # Handle randomization
            if randomize and password:
                seed = hash(password) & 0x7FFFFFFF

            # Encode
            pixels = img_ops.get_px_data(self.loaded_image)

            if isinstance(data_to_hide, str):
                new_pixels = enc.encode_msg(
                    pixels,
                    data_to_hide,
                    compress=compress,
                    seed=seed
                )
            else:
                # If encrypted (bytes), encode to base64 string for embedding
                import base64
                encrypted_b64 = base64.b64encode(data_to_hide).decode('ascii')
                msg_data = "__ENCRYPTED__" + encrypted_b64

                new_pixels = enc.encode_msg(
                    pixels,
                    msg_data,
                    compress=compress,
                    seed=seed
                )

            self.progress_enc.stop()

            if new_pixels is None:
                messagebox.showerror("Error", "Message too large for this image.")
                return

            # Save image
            new_img = img_ops.img_create_from_px(new_pixels, self.loaded_image.size)
            out_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")],
                title="Save encoded image"
            )

            if not out_path:
                return

            if img_ops.save_img(new_img, out_path):
                messagebox.showinfo(
                    "Success",
                    f"Image saved successfully!\n\nFile: {Path(out_path).name}"
                )
                self.msg_entry.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Could not save the image.")

    def decode_message(self):
        """Decode message from image."""
        if not self.loaded_image:
            messagebox.showerror("Error", "No image selected.")
            return

        self.progress_dec.start()
        self.root.update()

        extract_type = self.extract_var.get()
        use_decrypt = self.decrypt_var.get()
        use_seed = self.use_seed_var.get()

        seed = None
        if use_seed:
            seed_str = simpledialog.askstring("Seed", "Enter seed value:")
            if seed_str:
                try:
                    seed = int(seed_str)
                except ValueError:
                    seed = hash(seed_str) & 0x7FFFFFFF

        pixels = img_ops.get_px_data(self.loaded_image)
        message = None

        # Try to decode as text
        if extract_type in ["auto", "text"]:
            message = dec.decode_msg(pixels, seed=seed)

        self.progress_dec.stop()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)

        if message:
            # Check if encrypted
            if use_decrypt and message.startswith("__ENCRYPTED__"):
                password = simpledialog.askstring(
                    "Decryption",
                    "Enter password:",
                    show="*"
                )
                if password:
                    # Extract base64 encrypted data (remove __ENCRYPTED__ prefix)
                    import base64
                    try:
                        encrypted_b64 = message[len("__ENCRYPTED__"):]
                        encrypted_bytes = base64.b64decode(encrypted_b64)
                        decrypted = crypto.decrypt_message(encrypted_bytes, password)
                        if decrypted:
                            self.result_text.insert("1.0", decrypted)
                        else:
                            self.result_text.insert(
                                "1.0",
                                "Decryption failed. Wrong password?"
                            )
                            self.result_text.config(fg=self.error)
                    except Exception as e:
                        self.result_text.insert(
                            "1.0",
                            f"Decryption failed: {str(e)}"
                        )
                        self.result_text.config(fg=self.error)
            else:
                self.result_text.insert("1.0", message)
                messagebox.showinfo("Success", "Message extracted successfully!")
        else:
            self.result_text.insert("1.0", "(No hidden message found)")
            messagebox.showinfo("Result", "Could not extract any message from this image.")

        self.result_text.config(state=tk.DISABLED)

    def copy_result(self):
        """Copy result text to clipboard."""
        try:
            content = self.result_text.get("1.0", tk.END).strip()
            if content and content != "(No hidden message found)":
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                messagebox.showinfo("Success", "Copied to clipboard!")
            else:
                messagebox.showwarning("Warning", "No content to copy.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy: {e}")

    def setup_drag_drop(self):
        """Enable drag and drop for images (optional feature)."""
        try:
            from tkinterdnd2 import DND_FILES, DND_TEXT
            self.img_status_enc.drop_target_register(DND_FILES)
            self.img_status_enc.dnd_bind('<<Drop>>', self.drop_image_encode)
        except (ImportError, Exception):
            pass

    def drop_image_encode(self, event):
        files = event.data.split()
        if files:
            path = files[0].strip('{}')
            ext = Path(path).suffix.lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                self.image_path = path
                img = img_ops.load_img(path)
                if img:
                    self.loaded_image = img
                    name = Path(path).name
                    if len(name) > 40:
                        name = name[:37] + "..."
                    cap = enc.calculate_capacity(img.size)
                    self.img_status_enc.config(
                        text=f"{name} (capacity: ~{cap:,} chars)",
                        fg=self.success,
                        font=("Helvetica", 10, "bold")
                    )


def create_gui():
    root = tk.Tk()
    SteganographyGUI(root)
    return root


if __name__ == "__main__":
    create_gui()
