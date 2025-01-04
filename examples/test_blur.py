from PIL import Image
from pathlib import Path
from progressive_blur import apply_progressive_blur

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
                
                # Apply blur with custom parameters
                blurred_image = apply_progressive_blur(
                    original_image,
                    max_blur=50.0,
                    clear_until=0.15,
                    blur_start=0.25,
                    end_y=0.85
                )
                
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
