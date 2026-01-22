import argparse
from PIL import Image
import os
import sys

"""
Usage Example:
    python convert_bw.py input_image.png --width 120 --height 80 --threshold 100

Important Notes:
- If --width and --height are not specified, the script only converts the format 
  without modifying the image content, size, or position.
- Only when --width and --height are specified will the script scale the image 
  proportionally and add white padding.
- If dimensions are specified and the original aspect ratio differs from the 
  target, the image is scaled proportionally (maintaining aspect ratio) and 
  centered on a white background. No content is cropped.
"""

def resize_and_pad(image, output_size):
    """ Resize image and add white padding to meet the target resolution """
    original_width, original_height = image.size
    target_width, target_height = output_size
    
    # Calculate scaling factors
    scale_width = target_width / original_width
    scale_height = target_height / original_height
    
    # Use the smaller scale to ensure the image fits
    scale = min(scale_width, scale_height)
    
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    
    # Resize image
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Handle transparency
    if resized_image.mode == 'RGBA':
        white_bg = Image.new('RGB', (new_width, new_height), 'white')
        white_bg.paste(resized_image, mask=resized_image.split()[3])
        resized_image = white_bg
    elif resized_image.mode != 'RGB':
        resized_image = resized_image.convert('RGB')
    
    # Create padded image
    padded_image = Image.new('RGB', output_size, 'white')
    
    # Center the image
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    
    padded_image.paste(resized_image, (paste_x, paste_y))
    
    return padded_image

def convert_to_bitmap(input_file, output_file, output_size=None, threshold=128):
    try:
        image = Image.open(input_file)
    except IOError:
        print(f"Error: Cannot open input file {input_file}")
        sys.exit(1)

    if output_size is not None:
        image = resize_and_pad(image, output_size)

    # Convert to grayscale then threshold
    gray_image = image.convert('L')
    bw_image = gray_image.point(lambda x: 255 if x > threshold else 0, '1')

    # Save as BMP
    try:
        bw_image.save(output_file, 'BMP')
    except IOError:
        print(f"Error: Cannot save output file {output_file}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Convert an image to a 1-bit bitmap.')
    parser.add_argument('input_file', type=str, help='Path to input image file')
    parser.add_argument('--width', type=int, default=None, help='Target width')
    parser.add_argument('--height', type=int, default=None, help='Target height')
    parser.add_argument('--threshold', type=int, default=128, help='Threshold for B/W conversion (0-255)')
    parser.add_argument('--output', type=str, default=None, help='Output filename or directory')

    args = parser.parse_args()

    input_path = os.path.abspath(args.input_file)
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        if os.path.isdir(args.output):
            # If output is a directory, use input filename inside it
            filename = os.path.splitext(os.path.basename(input_path))[0] + ".bmp"
            output_path = os.path.join(args.output, filename)
        else:
            output_path = args.output
    else:
        # Default: save to current directory with .bmp extension
        filename = os.path.splitext(os.path.basename(input_path))[0] + ".bmp"
        output_path = os.path.join(os.getcwd(), filename)

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_size = None
    if args.width and args.height:
        output_size = (args.width, args.height)

    convert_to_bitmap(input_path, output_path, output_size, args.threshold)
    
    print(f"Success! Converted {os.path.basename(input_path)} to {output_path}")

if __name__ == "__main__":
    main()
