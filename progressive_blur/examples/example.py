from PIL import Image
from progressive_blur import apply_progressive_blur
import os

def process_example_images():
    # Create output directory if it doesn't exist
    output_dir = "output_images"
    os.makedirs(output_dir, exist_ok=True)
    
    # Process example images
    for image_name in ["example_01.jpeg", "example_02.jpeg"]:
        try:
            # Load and process image
            print(f"Processing {image_name}...")
            original_image = Image.open(image_name)
            
            # Apply blur with custom parameters
            blurred_image = apply_progressive_blur(
                original_image,
                max_blur=50.0,
                clear_until=0.15,
                blur_start=0.25,
                end_y=0.85
            )
            
            # Save result
            output_path = os.path.join(output_dir, f"blurred_{image_name}")
            blurred_image.save(output_path, quality=95)
            print(f"Saved blurred image to {output_path}")
            
        except Exception as e:
            print(f"Error processing {image_name}: {str(e)}")

if __name__ == "__main__":
    process_example_images()
