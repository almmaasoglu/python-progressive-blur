from PIL import Image
from progressive_blur import apply_progressive_blur
import os

def test_progressive_blur():
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Test with default parameters
    print("Testing with default parameters...")
    image = Image.open("example_01.jpeg")
    blurred = apply_progressive_blur(image)
    blurred.save("output/default_blur.jpeg")
    print("✓ Default blur test completed")
    
    # Test with custom parameters
    print("\nTesting with custom parameters...")
    image = Image.open("example_02.jpeg")
    custom_blurred = apply_progressive_blur(
        image,
        max_blur=30.0,        # Less blur
        clear_until=0.3,      # Keep more of the top clear
        blur_start=0.4,       # Start blur later
        end_y=0.9            # End blur later
    )
    custom_blurred.save("output/custom_blur.jpeg")
    print("✓ Custom blur test completed")
    
    print("\nBlurred images have been saved in the 'output' directory:")
    print("- output/default_blur.jpeg")
    print("- output/custom_blur.jpeg")

if __name__ == "__main__":
    test_progressive_blur()
