import argparse
from PIL import Image
import os
import sys

def invert_image(image_path, output_path=None):
    """
    Invert colors of a 1-bit image.
    """
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: File not found {image_path}")
        return
    except Exception as e:
        print(f"Error: Cannot open image {image_path}. Reason: {e}")
        return
    
    if image.mode != '1':
        print("Warning: Image is not 1-bit. Converting to 1-bit before inversion.")
        image = image.convert('1')
    
    # Invert image
    inverted_image = image.point(lambda p: 255 - p)
    
    # Determine output path
    if output_path is None:
        input_dir = os.path.dirname(image_path)
        input_name = os.path.basename(image_path)
        input_name_without_ext = os.path.splitext(input_name)[0]
        output_path = os.path.join(input_dir, f"{input_name_without_ext}_inverted.bmp")
    
    # Save
    try:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        inverted_image.save(output_path)
        print(f"Success: Inverted image saved to {output_path}")
    except Exception as e:
        print(f"Error: Cannot save image to {output_path}. Reason: {e}")

def main():
    parser = argparse.ArgumentParser(description="Invert colors of an image (Black <-> White).")
    parser.add_argument("input_file", help="Path to the input image file")
    parser.add_argument("-o", "--output", help="Path to the output image file (optional)")
    
    args = parser.parse_args()
    
    input_path = os.path.abspath(args.input_file)
    output_path = args.output
    if output_path:
        output_path = os.path.abspath(output_path)

    invert_image(input_path, output_path)

if __name__ == "__main__":
    main()
