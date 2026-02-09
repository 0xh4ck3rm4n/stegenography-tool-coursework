# Steganography Tool

## Overview

Steganography tool is used for hiding secret information within the file that looks ordinary such as document, images, videos and audio files etc. The hidden data can only extracted by authorized party.

## Learning Objective

- Understanding data hiding techniques
- Learning to write function based code
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
├── LICENSE
├── README.md                # This file
├── cat-icon.ico             # App Icon
├── decode.py                # Message decoding script
├── encode.py                # Message encoding script
├── gui.py                   # GUI tkinter script
├── images                   # Contains images used in documentation
│   └── output.png
├── img_operation.py         # Image loading/saving operations
├── main.py                  # main file to run the app
├── requirements.txt         # required modules
└── test_steganography.py    # Unit Testing
```

## Run Locally

```bash
# Clone the repository
https://github.com/0xh4ck3rm4n/stegenography-tool-coursework.git
cd stegenography-tool-coursework

# You need a requirements file with dependencies
pip install -r requirements.txt

# Run code
python main.py

```

**Expected Output**

<img src="images/output.png" alt="Application GUI Interface" width='300' height='350'>

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
