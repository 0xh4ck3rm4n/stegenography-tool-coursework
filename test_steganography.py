# Testing module for the tool
import unittest
from PIL import Image
import img_operation as img_ops
import encode
import decode

# Test case for Image operation
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
        result = img_ops.img_validation(small_img)
        self.assertFalse(result)

    # This function is to check if successfully gets the data from the Image
    def test_get_pixel_data(self):
        pixel = img_ops.get_px_data(self.test_img)
        self.assertEqual(len(pixel), 10000)
        self.assertEqual(pixel[0], (255, 0, 0))

    # This function is to check if it successfully create image from the pixel data
    def test_create_image_from_pixel(self):
        pixels = [(255, 0, 0)] * 100
        img = img_ops.img_create_from_px(pixels, (10, 10))
        self.assertEqual(img.size, (10, 10))
        self. assertEqual(img.mode, 'RGB')

# Test case for Encoding Image
class TestSteganographyEncode(unittest.TestCase):

    # This function test if it converts text to binary
    def test_text_to_binary(self):
        result = encode.text_to_binary("A")
        self.assertEqual(result, "01000001")

        result = encode.text_to_binary("AB")
        self.assertEqual(len(result), 16)

    # This function test to set the LSB to 1
    def test_modify_pixel_to_one(self):
        result = encode.pixel_modify(10, '1')
        self.assertEqual(result & 1, 1)

    # This function test if the pixel can be modified and set to zero
    def test_modify_pixel_set_to_zero(self):
        result = encode.pixel_modify(11, '0')
        self.assertEqual(result & 1, 0)

    # This function test if the encode message has been successfully embedded
    def test_encode_message_success(self):
        pixels = [(100, 100, 100)] * 1000
        message = "Hello"
        result = encode.encode_msg(pixels, message)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1000)
    
    # This function test if the encode message is too large to fit in an image
    def test_encode_message_too_large(self):
        pixels = [(100, 100, 100)] * 1000
        message = "This is a long long message" * 100
        result = encode.encode_msg(pixels, message)
        self.assertIsNone(result)
    
    # This function is to test for calculating capacity
    def test_calculate_capacity(self):
        capacity = encode.calculate_capacity((100, 100))
        self.assertGreater(capacity, 0)
        self.assertIsInstance(capacity, int)


# Test case for Decoding Image
class TestSteganographyDecode(unittest.TestCase):
    pass

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests()

        