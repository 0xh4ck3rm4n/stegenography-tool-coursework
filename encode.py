# Encoding script - handles image and merge the text into image

# function to convert text to binary
def text_to_binary(txt):
    binary = ''
    for char in txt:
        binary += format(ord(char), '08b')
    return binary

# function to modify LSB
def pixel_modify(pixel, bits):
    if bits == 1:
        # Setting LSB to 1
        return pixel | 1
    else:
        # Setting LSB to 0
        return pixel & ~1

# function to encode the message into pixel
def encode_msg(pixels, message):
    message = message + "###END###"
    binary_msg = text_to_binary(message)

    # checking if msg fits in image
    max_bytes = len(pixels) * 3
    if len(binary_msg) > max_bytes:
        return None
    
    # creating new list of pixels
    new_pixels = []
    msg_index = 0
    msg_len = len(binary_msg)

    for pixel in pixels:
        r, g, b = pixels

        if msg_index < msg_len:
            r = pixel_modify(r, binary_msg[msg_index])
            msg_index += 1

        if msg_index < msg_len:
            g = pixel_modify(g, binary_msg[msg_index])
            msg_index += 1

        if msg_index < msg_len:
            b = pixel_modify(b, binary_msg[msg_index])
            msg_index += 1

        new_pixels.append((r, g, b))

    return new_pixels

# function to calculate the maximum capacity of text to be merged in an image
def calculate_capacity(img_size):
    # img_size : takes width and height as an argument
    width, height = img_size
    total_px = width * height
    # Pixel is divided into 3 segments, and each char has 8 bits
    maximum_characters = (total_px * 3) // 8 - 10
    return maximum_characters