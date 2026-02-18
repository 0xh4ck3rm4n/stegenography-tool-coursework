# Testing module for the tool
import unittest
from PIL import Image
import img_operation as img_ops
import encode
import decode
import crypto
import compression


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
        self.assertEqual(img.mode, 'RGB')


# Test case for Encoding Image
class TestSteganographyEncode(unittest.TestCase):

    # This function test if it converts text to binary
    def test_text_to_binary(self):
        result = encode.text_to_binary("A")
        self.assertEqual(result, "01000001")

    # This function test if it converts text to binary with multiple character
    def test_text_to_binary_multiple(self):
        result = encode.text_to_binary("AB")
        self.assertEqual(result, "0100000101000010")

    # This function test if it encode message in pixel
    def test_encode_msg(self):
        pixels = [(100, 100, 100)] * 100
        result = encode.encode_msg(pixels, "Hi")
        self.assertIsNotNone(result)

    # This function test if encode_msg returns None when message is too long
    def test_encode_msg_too_long(self):
        pixels = [(100, 100, 100)] * 10
        result = encode.encode_msg(pixels, "A" * 1000)
        self.assertIsNone(result)

    # This function test if it converts bytes to binary
    def test_bytes_to_binary(self):
        result = encode.bytes_to_binary(b"A")
        self.assertEqual(result, "01000001")

    # This function test if it converts binary to bytes
    def test_binary_to_bytes(self):
        result = encode.binary_to_bytes("0100000101000010")
        self.assertEqual(result, b"AB")

    # This function test the capacity calculation
    def test_calculate_capacity(self):
        result = encode.calculate_capacity((100, 100))
        self.assertGreater(result, 100)

    # This function test encode with seed
    def test_encode_msg_with_seed(self):
        pixels = [(100, 100, 100)] * 100
        result = encode.encode_msg(pixels, "Test", seed=12345)
        self.assertIsNotNone(result)


# Test case for Decoding Image
class TestSteganographyDecode(unittest.TestCase):

    # This function test if it extract LSB from pixel
    def test_extract_lsb(self):
        result = decode.extract_lsb(5)  # Binary: 101, LSB = 1
        self.assertEqual(result, "1")

    # This function test if it extract LSB from even pixel
    def test_extract_lsb_even(self):
        result = decode.extract_lsb(4)  # Binary: 100, LSB = 0
        self.assertEqual(result, "0")

    # This function test if it converts binary to text
    def test_binary_to_txt(self):
        binary = '01000001'
        result = decode.binary_to_txt(binary)
        self.assertEqual(result, "A")

    # This function test binary to text with multiple character
    def test_binary_to_txt_multiple(self):
        binary = '0100000101000010'
        result = decode.binary_to_txt(binary)
        self.assertEqual(result, "AB")
    
    # This function test decode message with proper delimiter
    def test_decode_msg_within_delimiter(self):
        test_img = Image.new('RGB', (100, 100))
        pixels = list(test_img.get_flattened_data())

        message = "Test"
        encoded_pixels = encode.encode_msg(pixels, message)

        if encoded_pixels:
            decoded = decode.decode_msg(encoded_pixels)
            self.assertEqual(decoded, message)

    # This function test if it is possible to decode message with no delimiter
    def test_decode_msg_no_delimiter(self):
        pixels = [(100, 100, 100)] * 100
        result = decode.decode_msg(pixels)
        self.assertIsNone(result)

    # This function test decode with seed
    def test_decode_msg_with_seed(self):
        test_img = Image.new('RGB', (100, 100))
        pixels = list(test_img.get_flattened_data())

        message = "Secret"
        seed = 12345
        encoded_pixels = encode.encode_msg(pixels, message, seed=seed)
        
        if encoded_pixels:
            decoded = decode.decode_msg(encoded_pixels, seed=seed)
            self.assertEqual(decoded, message)


# Test case for Cryptography
class TestCrypto(unittest.TestCase):

    # Test password-based key derivation
    def test_derive_key_from_password(self):
        key, salt = crypto.derive_key_from_password("test_password")
        self.assertIsNotNone(key)
        self.assertEqual(len(salt), 16)

    # Test same password produces same key with same salt
    def test_derive_key_consistency(self):
        salt = b'0123456789abcdef'
        key1, _ = crypto.derive_key_from_password("test", salt)
        key2, _ = crypto.derive_key_from_password("test", salt)
        self.assertEqual(key1, key2)

    # Test encrypt and decrypt message
    def test_encrypt_decrypt_message(self):
        message = "Secret Message"
        password = "my_password"
        encrypted = crypto.encrypt_message(message, password)
        self.assertIsNotNone(encrypted)
        
        decrypted = crypto.decrypt_message(encrypted, password)
        self.assertEqual(decrypted, message)

    # Test decrypt with wrong password
    def test_decrypt_wrong_password(self):
        message = "Secret Message"
        password = "correct_password"
        encrypted = crypto.encrypt_message(message, password)
        
        decrypted = crypto.decrypt_message(encrypted, "wrong_password")
        self.assertIsNone(decrypted)


# Test case for Compression
class TestCompression(unittest.TestCase):

    # Test zlib compression
    def test_compress_zlib(self):
        data = b"A" * 100
        compressed = compression.compress_data(data, method='zlib')
        self.assertLess(len(compressed), len(data))

    # Test zlib decompression
    def test_decompress_zlib(self):
        original = b"Test data for compression"
        compressed = compression.compress_data(original, method='zlib')
        decompressed = compression.decompress_data(compressed, method='zlib')
        self.assertEqual(decompressed, original)

    # Test compression ratio calculation
    def test_compression_ratio(self):
        ratio = compression.get_compression_ratio(1000, 700)
        self.assertAlmostEqual(ratio, 30.0, places=1)


# Test case for Integration
class TestIntegration(unittest.TestCase):

    # This function test for the full encode and decode cycle
    def test_encode_decode_cycle(self):
        test_img = Image.new('RGB', (100, 100), color='blue')
        pixels = list(test_img.get_flattened_data())

        message = "Secret Message"
        encoded_pixels = encode.encode_msg(pixels, message)
        self.assertIsNotNone(encoded_pixels)

        decoded_message = decode.decode_msg(encoded_pixels)
        self.assertEqual(decoded_message, message)
    
    # This function test for the full encode and decode cycle with special character
    def test_encode_decode_cycle_with_special_character(self):
        test_img = Image.new('RGB', (100, 100), color='blue')
        pixels = list(test_img.get_flattened_data())

        message = "Hii %^&**@#$"
        encoded_pixels = encode.encode_msg(pixels, message)
        self.assertIsNotNone(encoded_pixels)

        decoded_message = decode.decode_msg(encoded_pixels)
        self.assertEqual(decoded_message, message)

    # Test encode and decode with compression
    def test_encode_decode_with_compression(self):
        test_img = Image.new('RGB', (200, 200))
        pixels = list(test_img.get_flattened_data())

        message = "Compressed message test"
        encoded_pixels = encode.encode_msg(pixels, message, compress=True)
        self.assertIsNotNone(encoded_pixels)

        decoded = decode.decode_msg(encoded_pixels)
        self.assertEqual(decoded, message)

    # Test encode and decode with seed
    def test_encode_decode_with_seed(self):
        test_img = Image.new('RGB', (100, 100))
        pixels = list(test_img.get_flattened_data())

        message = "Seeded message"
        seed = 42
        encoded_pixels = encode.encode_msg(pixels, message, seed=seed)
        self.assertIsNotNone(encoded_pixels)

        decoded = decode.decode_msg(encoded_pixels, seed=seed)
        self.assertEqual(decoded, message)

    # Test full workflow with encryption
    def test_full_workflow_encrypted(self):
        # 1. Create message and password
        message = "Confidential Data"
        password = "secure_pass"
        
        # 2. Encrypt message
        encrypted = crypto.encrypt_message(message, password)
        self.assertIsNotNone(encrypted)
        
        # 3. Prepare image
        test_img = Image.new('RGB', (200, 200))
        pixels = list(test_img.get_flattened_data())
        
        # 4. Encode encrypted data (as base64 to embed as text)
        import base64
        encrypted_b64 = base64.b64encode(encrypted).decode('ascii')
        
        # 5. Embed in image
        encoded_pixels = encode.encode_msg(pixels, encrypted_b64)
        self.assertIsNotNone(encoded_pixels)
        
        # 6. Decode from image
        decoded_b64 = decode.decode_msg(encoded_pixels)
        self.assertEqual(decoded_b64, encrypted_b64)
        
        # 7. Decrypt message
        extracted_encrypted = base64.b64decode(decoded_b64)
        decrypted = crypto.decrypt_message(extracted_encrypted, password)
        self.assertEqual(decrypted, message)

    # Test file encoding and decoding
    def test_file_encode_decode(self):
        import tempfile
        import os
        
        # Create temporary file with test data
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
            tmp.write(b"Test file content for steganography")
            tmp_path = tmp.name
        
        try:
            # Encode file
            test_img = Image.new('RGB', (500, 500))
            pixels = list(test_img.get_flattened_data())
            
            encoded_pixels = encode.encode_file(pixels, tmp_path)
            self.assertIsNotNone(encoded_pixels)
            
            # Decode file
            output_path = tmp_path + '.extracted'
            success = decode.decode_file(encoded_pixels, output_path)
            self.assertTrue(success)
            
            # Verify content
            with open(output_path, 'rb') as f:
                extracted_content = f.read()
            
            with open(tmp_path, 'rb') as f:
                original_content = f.read()
            
            self.assertEqual(extracted_content, original_content)
            
            # Cleanup
            if os.path.exists(output_path):
                os.remove(output_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests()

