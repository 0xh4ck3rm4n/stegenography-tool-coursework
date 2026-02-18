# Script to decode the message out of the image
import random
import compression
import encode as enc


# extract least significant bit from pixel value
def extract_lsb(pixel_value):
    return str(pixel_value & 1)


# convert binary to text
def binary_to_txt(binary_str):
    text = ''
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text


# decode message from the pixel data
def decode_msg(img_pixel, seed=None):
    # Create pixel order (same as encoding)
    if seed is not None:
        random.seed(seed)
        pixel_indices = list(range(len(img_pixel)))
        random.shuffle(pixel_indices)
    else:
        pixel_indices = list(range(len(img_pixel)))

    binary_message = ''
    for idx in pixel_indices:
        pixel = img_pixel[idx]
        r, g, b = pixel
        binary_message += extract_lsb(r)
        binary_message += extract_lsb(g)
        binary_message += extract_lsb(b)

    # Extract compression flag (first byte)
    if len(binary_message) < 8:
        return None

    compression_flag = binary_message[:8]
    data_binary = binary_message[8:]

    # Check for compression flag
    if compression_flag == '11111111':  # Compressed
        # Find trailer (4 null bytes)
        trailer = '00000000' * 4
        if trailer in data_binary:
            data_binary = data_binary[:data_binary.index(trailer)]

        try:
            compressed_data = enc.binary_to_bytes(data_binary)
            decompressed = compression.decompress_data(compressed_data)
            return decompressed.decode() if decompressed else None
        except Exception:
            return None

    elif compression_flag == '00000000':  # Not compressed
        decoded_text = binary_to_txt(data_binary)

        # Find end marker (4 null bytes = 4 null characters)
        end_marker = '\x00\x00\x00\x00'
        if end_marker in decoded_text:
            message = decoded_text.split(end_marker)[0]
            return message if message else None
        else:
            return None

    else:
        return None


# decode file from pixel data
def decode_file(img_pixel, output_path, seed=None):
    try:
        # Create pixel order (same as encoding)
        if seed is not None:
            random.seed(seed)
            pixel_indices = list(range(len(img_pixel)))
            random.shuffle(pixel_indices)
        else:
            pixel_indices = list(range(len(img_pixel)))

        binary_data = ''
        for idx in pixel_indices:
            pixel = img_pixel[idx]
            r, g, b = pixel
            binary_data += extract_lsb(r)
            binary_data += extract_lsb(g)
            binary_data += extract_lsb(b)

        # Extract file flag (first byte should be 0xAA = 10101010)
        if len(binary_data) < 8 or binary_data[:8] != '10101010':
            return False

        data_binary = binary_data[8:]

        # Find trailer (4 null bytes)
        trailer = '00000000' * 4
        if trailer in data_binary:
            data_binary = data_binary[:data_binary.index(trailer)]

        compressed_data = enc.binary_to_bytes(data_binary)
        decompressed = compression.decompress_data(compressed_data)

        if decompressed:
            with open(output_path, 'wb') as f:
                f.write(decompressed)
            return True
        return False

    except Exception:
        return False


# to check if pixels contain message data
def check_if_msg_exist(pixels, seed=None):
    try:
        if seed is not None:
            random.seed(seed)
            pixel_indices = list(range(len(pixels)))
            random.shuffle(pixel_indices)
        else:
            pixel_indices = list(range(len(pixels)))

        binary_data = ''
        check_count = min(len(pixels), 500)

        for i in range(check_count):
            idx = pixel_indices[i]
            r, g, b = pixels[idx]
            binary_data += extract_lsb(r)
            binary_data += extract_lsb(g)
            binary_data += extract_lsb(b)

        # Check for valid compression flags in first byte
        if len(binary_data) >= 8:
            flag = binary_data[:8]
            # Valid flags: 11111111 (compressed), 00000000 (plain), 10101010 (file)
            return flag in ['11111111', '00000000', '10101010']

        return False
    except Exception:
        return False
