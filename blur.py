from PIL import Image, ImageFilter
from io import BytesIO
import numpy as np
import os
from pathlib import Path

def apply_progressive_blur(image):
    # Convert image to PIL Image if it's bytes
    if isinstance(image, bytes):
        image = Image.open(BytesIO(image))
    
    # Create base image
    width, height = image.size
    result = image.copy()
    
    # Create a gradient mask for the blur intensity
    mask = Image.new('L', (width, height))
    mask_data = np.array(mask)
    
    # Adjusted blur parameters
    max_blur = 50.0
    clear_until = 0.15   # Keep completely clear until 15% from top
    blur_start = 0.25    # Start blur at 25% from top
    end_y = 0.85         # End blur at 85% from top
    
    # Create the blur intensity gradient
    for y in range(height):
        y_percent = y / height
        if y_percent < clear_until:
            # Completely clear at top
            blur_intensity = 0
        elif y_percent < blur_start:
            # Smooth transition from clear to blur
            progress = (y_percent - clear_until) / (blur_start - clear_until)
            blur_intensity = int(255 * (0.3 * progress))
        elif y_percent > end_y:
            blur_intensity = 255
        else:
            # Calculate progressive blur intensity
            progress = (y_percent - blur_start) / (end_y - blur_start)
            blur_intensity = int(255 * (0.3 + (0.7 * progress)))
        mask_data[y, :] = blur_intensity
    
    # Convert back to PIL Image
    blur_mask = Image.fromarray(mask_data)
    
    # Create maximally blurred version
    blurred = image.filter(ImageFilter.GaussianBlur(radius=max_blur))
    
    # Composite original and blurred images using the gradient mask
    result = Image.composite(blurred, image, blur_mask)
    
    return result

def test_blur_images():
    # Create input/output directories
    input_dir = Path("test_images")
    output_dir = Path("output_images")
    output_dir.mkdir(exist_ok=True)
    
    # Added WebP to supported formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.webp'}
    
    # Process each image in the input directory
    for image_path in input_dir.iterdir():
        if image_path.suffix.lower() in supported_formats:
            try:
                # Load and process image
                print(f"Processing {image_path.name}...")
                original_image = Image.open(image_path)
                
                # Convert to RGBA if WebP has transparency
                if image_path.suffix.lower() == '.webp' and original_image.mode == 'RGBA':
                    # Preserve alpha channel
                    original_image = original_image.convert('RGBA')
                
                # Apply blur
                blurred_image = apply_progressive_blur(original_image)
                
                # Save result
                output_path = output_dir / f"blurred_{image_path.name}"
                
                # Save with appropriate format and quality
                if output_path.suffix.lower() == '.webp':
                    blurred_image.save(output_path, 'WEBP', quality=90, lossless=False)
                else:
                    blurred_image.save(output_path)
                    
                print(f"Saved blurred image to {output_path}")
                
            except Exception as e:
                print(f"Error processing {image_path.name}: {str(e)}")

if __name__ == "__main__":
    test_blur_images() 