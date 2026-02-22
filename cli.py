import argparse
import sys
from encode import encode_message
from decode import decode_message

def run():
    parser = argparse.ArgumentParser(
        prog="steganography-tool",
        description="Hide or extract secret messages in images"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    enc = subparsers.add_parser("encode", help="Hide a message inside an image")
    enc.add_argument("--image",   required=True, help="Path to input image")
    enc.add_argument("--message", required=True, help="Secret message to hide")
    enc.add_argument("--output",  required=True, help="Path to save output image")
    enc.add_argument("--password", default=None, help="Optional encryption password")

    dec = subparsers.add_parser("decode", help="Extract a hidden message from an image")
    dec.add_argument("--image",    required=True, help="Path to stego image")
    dec.add_argument("--password", default=None, help="Password if message was encrypted")

    args = parser.parse_args()

    if args.command == "encode":
        try:
            encode_message(args.image, args.message, args.output, args.password)
            print(f"Message hidden successfully → {args.output}")
        except Exception as e:
            print(f"Encoding failed: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "decode":
        try:
            message = decode_message(args.image, args.password)
            print(f"Hidden message: {message}")
        except Exception as e:
            print(f"Decoding failed: {e}", file=sys.stderr)
            sys.exit(1)