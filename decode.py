# Script to decode the message out of the image

# extract least significant bit from pixel value
def extract_lsb(pixel_value):
    return str(pixel_value & 1)

# convert binary to text
def binary_to_txt(binary_str):
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

# decode message from the pixel data
def decode_msg(img_pixel):
    binary_message = ''
    
    for pixel in img_pixel:
        r, g, b = pixel
        binary_message += extract_lsb(r)
        binary_message += extract_lsb(g)
        binary_message += extract_lsb(b)
    
    decoded_text = binary_to_txt(binary_message)
    
    delimiter = "###END###"
    if delimiter in decoded_text:
        message = decoded_text.split(delimiter)[0]
        return message
    else:
        return None

# to check if pixels contain message data
def check_if_msg_exist(pixels):
    binary_data = ''
    check_pixels = min(len(pixels), 500)
    
    for i in range(check_pixels):
        r, g, b = pixels[i]
        binary_data += extract_lsb(r)
        binary_data += extract_lsb(g)
        binary_data += extract_lsb(b)
    
    text = binary_to_txt(binary_data)
    return "###END###" in text
