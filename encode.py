# Encoding script - handles image and merge the text into image

# function to convert text to binary
def text_to_binary(txt):
    binary = ''
    for char in txt:
        binary += format(ord(char), '08b')
    return binary

# function to modify LSB
def pixel_modify(pixel, bits):
    pass

# function to encode the message into pixel
def encode_msg(pixel, message):
    pass

# function to calculate the maximum capacity of text to be merged in an image
def calculate_capacity(img_size):
    pass