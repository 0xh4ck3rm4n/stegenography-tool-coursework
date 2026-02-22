# Encoding script - handles image and merge the text into image
import random
import compression

# function to convert text to binary
def text_to_binary(txt):
    binary = ''
    for char in txt:
        binary += format(ord(char), '08b')
    return binary

# function to convert bytes to binary
def bytes_to_binary(data: bytes) -> str:
    binary = ''
    for byte in data:
        binary += format(byte, '08b')
    return binary

# function to convert binary string to bytes
def binary_to_bytes(binary_str: str) -> bytes:
    byte_array = bytearray()
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) == 8:
            byte_array.append(int(byte, 2))
    return bytes(byte_array)

# function to modify LSB
def pixel_modify(pixel, bits):
    if bits == '1':
        # Setting LSB to 1
        return pixel | 1
    else:
        # Setting LSB to 0
        return pixel & ~1


# function to encode the message into pixel with optional compression and seed
def encode_msg(pixels, message, compress=False, seed=None):

    # Add compression flag and delimiter
    if compress:
        message_bytes = compression.compress_data(message.encode())
        # Prepend 0xFF to indicate compression
        binary_msg = '11111111' + bytes_to_binary(message_bytes) + '00000000' * 4
    else:
        # Prepend 0x00 to indicate no compression
        binary_msg = '00000000' + text_to_binary(message) + '00000000' * 4

    # checking if msg fits in image
    max_bits = len(pixels) * 3
    if len(binary_msg) > max_bits:
        return None

    # Create randomized pixel order if seed provided
    if seed is not None:
        random.seed(seed)
        pixel_indices = list(range(len(pixels)))
        random.shuffle(pixel_indices)
    else:
        pixel_indices = list(range(len(pixels)))

    # creating new list of pixels
    new_pixels = pixels.copy()
    msg_index = 0
    msg_len = len(binary_msg)

    for idx in pixel_indices:
        if msg_index >= msg_len:
            break

        pixel = pixels[idx]
        r, g, b = pixel

        if msg_index < msg_len:
            r = pixel_modify(r, binary_msg[msg_index])
            msg_index += 1

        if msg_index < msg_len:
            g = pixel_modify(g, binary_msg[msg_index])
            msg_index += 1

        if msg_index < msg_len:
            b = pixel_modify(b, binary_msg[msg_index])
            msg_index += 1

        new_pixels[idx] = (r, g, b)

    return new_pixels


# function to encode file data
def encode_file(pixels, file_path, seed=None):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Compress file data
        compressed_data = compression.compress_data(file_data)

        # Prepend compression flag
        binary_data = '10101010' + bytes_to_binary(compressed_data) + '00000000' * 4

        max_bits = len(pixels) * 3
        if len(binary_data) > max_bits:
            return None

        # Create randomized pixel order if seed provided
        if seed is not None:
            random.seed(seed)
            pixel_indices = list(range(len(pixels)))
            random.shuffle(pixel_indices)
        else:
            pixel_indices = list(range(len(pixels)))

        new_pixels = pixels.copy()
        msg_index = 0
        msg_len = len(binary_data)

        for idx in pixel_indices:
            if msg_index >= msg_len:
                break

            pixel = pixels[idx]
            r, g, b = pixel

            if msg_index < msg_len:
                r = pixel_modify(r, binary_data[msg_index])
                msg_index += 1

            if msg_index < msg_len:
                g = pixel_modify(g, binary_data[msg_index])
                msg_index += 1

            if msg_index < msg_len:
                b = pixel_modify(b, binary_data[msg_index])
                msg_index += 1

            new_pixels[idx] = (r, g, b)

        return new_pixels
    except Exception:
        return None


# function to calculate the maximum capacity of text to be merged in an image
def calculate_capacity(img_size):
    # img_size : takes width and height as an argument
    width, height = img_size
    total_px = width * height
    # Pixel is divided into 3 segments, and each char has 8 bits
    # Account for 1 byte header + 4 bytes trailer
    maximum_characters = (total_px * 3) // 8 - 5
    return maximum_characters