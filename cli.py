import argparse
import sys
import img_operation as img_op
import encode as enc
import decode as dec

def run():
    parser = argparse.ArgumentParser(
        prog="steganography-tool",
        description="Hide or extract secret messages in images"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Encode ---
    e = subparsers.add_parser("encode", help="Hide a message inside an image")
    e.add_argument("--image",    required=True, help="Path to input image")
    e.add_argument("--message",  required=True, help="Secret message to hide")
    e.add_argument("--output",   required=True, help="Path to save output image")
    e.add_argument("--compress", action="store_true", help="Compress the message")
    e.add_argument("--seed",     default=None, type=int, help="Random seed for pixel order")

    # --- Decode ---
    d = subparsers.add_parser("decode", help="Extract a hidden message from an image")
    d.add_argument("--image", required=True, help="Path to stego image")
    d.add_argument("--seed",  default=None, type=int, help="Seed used during encoding")

    # --- Capacity ---
    c = subparsers.add_parser("capacity", help="Check how many characters an image can hold")
    c.add_argument("--image", required=True, help="Path to image")

    args = parser.parse_args()

    if args.command == "encode":
        # Load image using your actual function names
        img = img_op.load_img(args.image)
        if img is None:
            print(f"[✗] Could not load image: {args.image}", file=sys.stderr)
            sys.exit(1)

        # Convert to RGB if needed, then validate
        if img.mode != 'RGB':
            img = img.convert('RGB')

        if not img_op.img_validation(img):
            print("[✗] Image is invalid (must be RGB, at least 10x10)", file=sys.stderr)
            sys.exit(1)

        pixels = img_op.get_px_data(img)
        img_size = img.size

        capacity = enc.calculate_capacity(img_size)
        if len(args.message) > capacity:
            print(f"[✗] Message too long ({len(args.message)} chars). Max: {capacity}", file=sys.stderr)
            sys.exit(1)

        new_pixels = enc.encode_msg(pixels, args.message, compress=args.compress, seed=args.seed)
        if new_pixels is None:
            print("[✗] Encoding failed — message too large for image", file=sys.stderr)
            sys.exit(1)

        new_img = img_op.img_create_from_px(new_pixels, img_size)
        success = img_op.save_img(new_img, args.output)
        if success:
            print(f"[✓] Message hidden successfully → {args.output}")
        else:
            print("[✗] Failed to save image", file=sys.stderr)
            sys.exit(1)

    elif args.command == "decode":
        img = img_op.load_img(args.image)
        if img is None:
            print(f"[✗] Could not load image: {args.image}", file=sys.stderr)
            sys.exit(1)

        if not img_op.img_validation(img):
            print("[✗] Image is invalid or not RGB", file=sys.stderr)
            sys.exit(1)

        pixels = img_op.get_px_data(img)

        message = dec.decode_msg(pixels, seed=args.seed)
        if message:
            print(f"[✓] Hidden message: {message}")
        else:
            print("[✗] No hidden message found", file=sys.stderr)
            sys.exit(1)

    elif args.command == "capacity":
        img = img_op.load_img(args.image)
        if img is None:
            print(f"[✗] Could not load image: {args.image}", file=sys.stderr)
            sys.exit(1)

        capacity = enc.calculate_capacity(img.size)
        width, height = img.size
        print(f"[✓] Image size: {width}x{height}")
        print(f"[✓] Max capacity: {capacity} characters")