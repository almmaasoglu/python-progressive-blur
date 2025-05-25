#!/usr/bin/env python3
"""
Simple example demonstrating basic progressive blur usage.

This script shows how to:
- Apply progressive blur to images
- Use different presets
- Handle various image formats
- Process multiple images
"""

from pathlib import Path
from PIL import Image
from progressive_blur import apply_progressive_blur, apply_preset, BLUR_PRESETS


def create_test_image():
    """Create a simple test image if none exists."""
    img = Image.new('RGB', (800, 600), color='lightblue')
    
    # Add some simple shapes for visual effect
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Draw rectangles
    draw.rectangle([100, 100, 300, 200], fill='red')
    draw.rectangle([400, 200, 600, 300], fill='green')
    draw.rectangle([200, 350, 500, 450], fill='blue')
    
    # Add text
    draw.text((50, 50), "Progressive Blur Test", fill='black')
    
    return img


def test_basic_blur():
    """Test basic progressive blur functionality."""
    print("Testing basic progressive blur...")
    
    # Create or use test image
    test_images_dir = Path("test_images")
    output_dir = Path("output_images")
    output_dir.mkdir(exist_ok=True)
    
    # If no test images directory exists, create a test image
    if not test_images_dir.exists():
        test_images_dir.mkdir()
        test_img = create_test_image()
        test_img.save(test_images_dir / "test_image.jpg", quality=95)
        print("Created test image: test_images/test_image.jpg")
    
    # Supported formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    
    # Process each image in the test directory
    for image_path in test_images_dir.iterdir():
        if image_path.suffix.lower() in supported_formats:
            try:
                print(f"Processing {image_path.name}...")
                
                # Load image
                original_image = Image.open(image_path)
                
                # Apply default progressive blur
                blurred_image = apply_progressive_blur(original_image)
                
                # Save result
                output_path = output_dir / f"blurred_{image_path.name}"
                
                # Handle different formats appropriately
                if output_path.suffix.lower() in ('.jpg', '.jpeg'):
                    blurred_image.save(output_path, quality=95, optimize=True)
                elif output_path.suffix.lower() == '.webp':
                    blurred_image.save(output_path, quality=90, method=6)
                else:
                    blurred_image.save(output_path)
                
                print(f"  Saved: {output_path}")
                
            except Exception as e:
                print(f"  Error processing {image_path.name}: {e}")


def test_presets():
    """Test different blur presets."""
    print("\nTesting blur presets...")
    
    # Create test image
    img = create_test_image()
    output_dir = Path("output_images/presets")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Available presets: {list(BLUR_PRESETS.keys())}")
    
    # Apply each preset
    for preset_name in BLUR_PRESETS.keys():
        try:
            result = apply_preset(img, preset_name)
            output_path = output_dir / f"preset_{preset_name}.jpg"
            result.save(output_path, quality=95)
            print(f"  Applied preset '{preset_name}': {output_path}")
        except Exception as e:
            print(f"  Error with preset '{preset_name}': {e}")


def test_custom_parameters():
    """Test custom blur parameters."""
    print("\nTesting custom parameters...")
    
    img = create_test_image()
    output_dir = Path("output_images/custom")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test different parameter combinations
    test_configs = [
        {
            'name': 'gentle_blur',
            'max_blur': 20.0,
            'clear_until': 0.3,
            'blur_start': 0.4,
            'end_position': 0.9
        },
        {
            'name': 'strong_blur',
            'max_blur': 60.0,
            'clear_until': 0.1,
            'blur_start': 0.2,
            'end_position': 0.7
        },
        {
            'name': 'center_focus',
            'max_blur': 40.0,
            'clear_until': 0.0,
            'blur_start': 0.2,
            'end_position': 0.8,
            'direction': 'edges_to_center'
        }
    ]
    
    for config in test_configs:
        try:
            name = config.pop('name')
            result = apply_progressive_blur(img, **config)
            output_path = output_dir / f"{name}.jpg"
            result.save(output_path, quality=95)
            print(f"  Applied custom config '{name}': {output_path}")
        except Exception as e:
            print(f"  Error with config '{name}': {e}")


def main():
    """Run all tests."""
    print("Progressive Blur - Simple Test Script")
    print("=" * 40)
    
    test_basic_blur()
    test_presets()
    test_custom_parameters()
    
    print("\n✅ All tests completed!")
    print("Check the 'output_images' directory for results.")


if __name__ == "__main__":
    main()
