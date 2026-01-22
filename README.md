# Image Processing Tools

A collection of Python scripts for processing images into 1-bit bitmaps, optimized for embedded displays (like E-Paper).

## Features

- **Convert to 1-Bit BMP**: Convert JPG/PNG to 1-bit monochrome BMP with optional resizing and padding.
- **Invert Colors**: Flip black and white pixels in 1-bit images.

## Requirements

- Python 3.x
- Pillow (PIL)

```bash
pip install Pillow
```

## Usage

### 1. Convert to 1-Bit BMP
Converts an image to a 1-bit bitmap. Supports proportional scaling with white padding if dimensions are specified.

```bash
python convert_bw.py input.png --width 120 --height 80 --threshold 128
```

- `--width`: (Optional) Target width.
- `--height`: (Optional) Target height.
- `--threshold`: (Optional) B/W threshold (0-255). Default is 128.

### 2. Invert Colors
Inverts the colors of a 1-bit image.

```bash
python invert_colors.py input.bmp -o output.bmp
```

## License
MIT
