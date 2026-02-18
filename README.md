# Steganography Tool

## Overview

In this project, a steganography tool is built using python and it's libraries. Steganography tool is used for hiding secret information within the file that looks ordinary such as document, images, videos and audio files etc. The hidden data can only be extracted by the authorized party.

## Learning Objective

- Understanding data hiding techniques
- Learning to write function-based code
- Identifying security use cases
- Learning version control and packaging
- Gaining knowledge of various data carriers
- Understanding secure message transmission

## Features

- Hides messages in image pixels
- Clean Tkinter interface
- Tests all modules individually and together
- Validates inputs and handles errors

## Project Structure

```
.
├── main.py                     # Entry point
├── gui.py                      # Main Tkinter GUI (v2.0 - tabbed interface)
├── encode.py                   # Enhanced encoding (compression, randomization)
├── decode.py                   # Enhanced decoding (compression, randomization)
├── crypto.py                   # NEW: Encryption/decryption utilities
├── compression.py              # NEW: Compression utilities
├── img_operation.py            # Image loading/saving operations
├── test_steganography.py       # Comprehensive unit tests (updated)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── images/                     # Sample images
```

## Installation

### Prerequisites

- Python 3.8+
- Tkinter (usually included with Python)

### Setup

```bash
# Clone the repository
git clone https://github.com/0xh4ck3rm4n/steganography-tool-coursework.git
cd steganography-tool-coursework

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

**Expected Output**

<img src="images/home-page.png" alt="Application GUI Interface" width='500' height='350'>

**Encode Image**

<img src="images/ENCODE-IMAGE.png" alt="Encode Message Function" width='500' height='350'>

**Decode Image**

<img src="images/decode-image.png" alt="Encode Message Function" width='500' height='350'>

## Running Tests

```bash
# Run all tests
python -m pytest test_steganography.py -v

# Or using unittest
python test_steganography.py

# Run specific test class
python -m pytest test_steganography.py::TestCrypto -v

# Run with coverage
pytest test_steganography.py --cov=.
```

## Pull and Run from GHCR

```bash
# Pull the latest image
docker pull ghcr.io/0xh4ck3rm4n/steganography-tool:latest

# Run the container
docker run ghcr.io/0xh4ck3rm4n/steganography-tool:latest
```

## Testing Features

## Author

- **Gaurav Poudel** - Initial work and demonstration

## License

This project is licensed under the MIT License - See [License](/LICENSE) for more details
