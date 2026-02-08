from PIL import Image

def get_flattened_data(self):
    """
    Returns flattened pixel data of the image.
    Each pixel is returned as an (R, G, B) tuple.
    """
    return list(self.getdata())
Image.Image.get_flattened_data = get_flattened_data

# load image from input path
def load_img(img_path):
    try:
        image = Image.open(img_path)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

# validate image for steganagraphy
def img_validation(img):
    if img is None:
        return False
    
    if img.mode != 'RGB':
        return False

    width, height = img.size
    if width < 10 or height < 10:
        return False
    return True

def get_px_data(img):
    pixels = list(img.get_flattened_data())
    return pixels

def img_create_from_px(px, size):
    img = Image.new('RGB', size)
    img.putdata(px)
    return img

def save_img(img, output_path):
    try:
        img.save(output_path, 'PNG')
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False