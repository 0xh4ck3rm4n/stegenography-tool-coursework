# Testing module for the tool
import unittest
from PIL import Image
import img_operation as img_ops
import encode
import decode

# TODO: Test function
class TestImageOperations(unittest.TestCase):
    # This function is for setting up the test
    def setUp(self):
        self.test_img = Image.new('RGB', (100, 100), color='red')

    # This function is to check for valid RGB test image
    def test_validate_img_valid(self):
        result = img_ops.img_validation(self.test_img)
        self.assertTrue(result)

    # This function is to check if it fails for the None image
    def test_validate_img_none(self):
        result = img_ops.img_validation(None)
        self.assertFalse(result)

    # This function is to check if it fails for the small image
    def test_validate_img_small(self):
        small_img = Image.new('RGB', (5, 5))
        result = img_ops.img_valid(small_img)
        self.assertFalse(result)

    # This function is to check if successfully gets the data from the Image
    def test_get_pixel_data(self):
        pixel = img_ops.get_px_data(self.test_image)
        self.assertEqual(len(pixel), 10000)
        self.assertEqual(pixel[0], (255, 0, 0))

    # This function is to check if it successfully create image from the pixel data
    def test_create_image_from_pixel(self):
        pixels = [(255, 0, 0)] * 100
        img = img_ops.img_create_from_px(pixels)
        self.assertEqual(img.size, (10, 10))
        self. assertEqual(img.mode, 'RGB')
        