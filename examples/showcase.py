#!/usr/bin/env python3
"""
Advanced examples demonstrating the capabilities of the Progressive Blur library.

This script showcases various features including:
- Different blur directions and algorithms
- Custom easing functions
- Preset usage
- Custom mask creation
- Batch processing
- Performance optimization
"""

import time
from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from progressive_blur import (
    apply_progressive_blur,
    apply_preset,
    batch_process_images,
    create_custom_blur_mask,
    apply_mask_based_blur,
    BlurDirection,
    BlurAlgorithm,
    EasingFunction,
    BLUR_PRESETS,
    optimize_image_for_web,
)


def create_sample_image(size: Tuple[int, int] = (800, 600)) -> Image.Image:
    """Create a sample image for testing."""
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw some geometric shapes
    draw.rectangle([50, 50, 200, 200], fill='red', outline='darkred', width=3)
    draw.ellipse([250, 100, 400, 250], fill='blue', outline='darkblue', width=3)
    draw.polygon([(500, 50), (600, 150), (450, 200)], fill='green', outline='darkgreen', width=3)
    
    # Add some text
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 36)
    except (OSError, IOError):
        # Fallback to default font
        font = ImageFont.load_default()
    
    draw.text((50, 300), "Progressive Blur Demo", fill='black', font=font)
    draw.text((50, 350), "High Quality Image Processing", fill='gray', font=font)
    
    # Add some gradient background
    for y in range(size[1]):
        color_value = int(255 * (y / size[1]) * 0.1)
        draw.line([(0, y), (size[0], y)], fill=(255-color_value, 255-color_value, 255))
    
    return img


def demo_basic_usage():
    """Demonstrate basic progressive blur usage."""
    print("🎯 Basic Usage Demo")
    print("-" * 50)
    
    # Create sample image
    img = create_sample_image()
    output_dir = Path("output/basic")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save original
    img.save(output_dir / "original.jpg", quality=95)
    
    # Apply default blur
    start_time = time.time()
    blurred = apply_progressive_blur(img)
    processing_time = time.time() - start_time
    
    blurred.save(output_dir / "default_blur.jpg", quality=95)
    print(f"✅ Default blur applied in {processing_time:.2f}s")
    
    # Apply custom blur
    custom_blur = apply_progressive_blur(
        img,
        max_blur=30.0,
        clear_until=0.2,
        blur_start=0.3,
        end_position=0.8
    )
    custom_blur.save(output_dir / "custom_blur.jpg", quality=95)
    print("✅ Custom blur parameters applied")


def demo_directions_and_algorithms():
    """Demonstrate different blur directions and algorithms."""
    print("\n🧭 Directions & Algorithms Demo")
    print("-" * 50)
    
    img = create_sample_image()
    output_dir = Path("output/directions_algorithms")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test different directions
    directions = [
        (BlurDirection.TOP_TO_BOTTOM, "top_to_bottom"),
        (BlurDirection.LEFT_TO_RIGHT, "left_to_right"),
        (BlurDirection.CENTER_TO_EDGES, "center_to_edges"),
        (BlurDirection.BOTTOM_TO_TOP, "bottom_to_top"),
    ]
    
    for direction, name in directions:
        result = apply_progressive_blur(
            img,
            max_blur=40.0,
            direction=direction,
            clear_until=0.1,
            blur_start=0.2,
            end_position=0.8
        )
        result.save(output_dir / f"direction_{name}.jpg", quality=95)
        print(f"✅ {name.replace('_', ' ').title()} direction")
    
    # Test different algorithms
    algorithms = [
        (BlurAlgorithm.GAUSSIAN, "gaussian"),
        (BlurAlgorithm.BOX, "box"),
        (BlurAlgorithm.MOTION, "motion"),
    ]
    
    for algorithm, name in algorithms:
        result = apply_progressive_blur(
            img,
            max_blur=35.0,
            algorithm=algorithm,
            direction=BlurDirection.TOP_TO_BOTTOM
        )
        result.save(output_dir / f"algorithm_{name}.jpg", quality=95)
        print(f"✅ {name.title()} algorithm")


def demo_easing_functions():
    """Demonstrate different easing functions."""
    print("\n📈 Easing Functions Demo")
    print("-" * 50)
    
    img = create_sample_image()
    output_dir = Path("output/easing")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    easing_functions = [
        (EasingFunction.LINEAR, "linear"),
        (EasingFunction.EASE_IN, "ease_in"),
        (EasingFunction.EASE_OUT, "ease_out"),
        (EasingFunction.EASE_IN_OUT, "ease_in_out"),
        (EasingFunction.EXPONENTIAL, "exponential"),
        (EasingFunction.SINE, "sine"),
    ]
    
    for easing, name in easing_functions:
        result = apply_progressive_blur(
            img,
            max_blur=50.0,
            easing=easing,
            clear_until=0.1,
            blur_start=0.2,
            end_position=0.9
        )
        result.save(output_dir / f"easing_{name}.jpg", quality=95)
        print(f"✅ {name.replace('_', ' ').title()} easing")


def demo_presets():
    """Demonstrate preset usage."""
    print("\n🎛️ Presets Demo")
    print("-" * 50)
    
    img = create_sample_image()
    output_dir = Path("output/presets")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Available presets: {list(BLUR_PRESETS.keys())}")
    
    for preset_name in BLUR_PRESETS.keys():
        result = apply_preset(img, preset_name)
        result.save(output_dir / f"preset_{preset_name}.jpg", quality=95)
        print(f"✅ Applied preset: {preset_name}")


def demo_custom_masks():
    """Demonstrate custom mask creation."""
    print("\n🎨 Custom Masks Demo")
    print("-" * 50)
    
    img = create_sample_image()
    output_dir = Path("output/custom_masks")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    width, height = img.size
    
    # Circular mask
    def circular_mask(x: int, y: int) -> float:
        center_x, center_y = width // 2, height // 2
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_distance = min(width, height) // 3
        return min(1.0, distance / max_distance)
    
    mask = create_custom_blur_mask(width, height, circular_mask)
    result = apply_mask_based_blur(img, mask, max_blur=40.0)
    result.save(output_dir / "circular_mask.jpg", quality=95)
    print("✅ Circular mask applied")
    
    # Diagonal gradient mask
    def diagonal_mask(x: int, y: int) -> float:
        return min(1.0, (x + y) / (width + height))
    
    mask = create_custom_blur_mask(width, height, diagonal_mask)
    result = apply_mask_based_blur(img, mask, max_blur=35.0)
    result.save(output_dir / "diagonal_mask.jpg", quality=95)
    print("✅ Diagonal gradient mask applied")
    
    # Checkerboard pattern
    def checkerboard_mask(x: int, y: int) -> float:
        block_size = 50
        checker_x = (x // block_size) % 2
        checker_y = (y // block_size) % 2
        return 1.0 if (checker_x + checker_y) % 2 else 0.0
    
    mask = create_custom_blur_mask(width, height, checkerboard_mask)
    result = apply_mask_based_blur(img, mask, max_blur=30.0)
    result.save(output_dir / "checkerboard_mask.jpg", quality=95)
    print("✅ Checkerboard pattern mask applied")


def demo_batch_processing():
    """Demonstrate batch processing capabilities."""
    print("\n🚀 Batch Processing Demo")
    print("-" * 50)
    
    # Create sample images
    input_dir = Path("output/batch_input")
    output_dir = Path("output/batch_output")
    input_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate different sample images
    for i in range(3):
        img = create_sample_image((600 + i*100, 400 + i*50))
        img.save(input_dir / f"sample_{i+1}.jpg", quality=95)
    
    print(f"Created {len(list(input_dir.glob('*.jpg')))} sample images")
    
    # Process batch with progress callback
    def progress_callback(current, total, input_path, output_path):
        print(f"  [{current}/{total}] {input_path.name} -> {output_path.name}")
    
    start_time = time.time()
    processed_files = batch_process_images(
        input_dir,
        output_dir,
        preset="dramatic",
        overwrite=True,
        progress_callback=progress_callback
    )
    processing_time = time.time() - start_time
    
    print(f"✅ Processed {len(processed_files)} images in {processing_time:.2f}s")


def demo_performance_comparison():
    """Demonstrate performance comparison between algorithms."""
    print("\n📊 Performance Comparison")
    print("-" * 50)
    
    # Create a larger test image
    img = create_sample_image((1920, 1080))
    
    algorithms = [
        (BlurAlgorithm.BOX, "Box Blur"),
        (BlurAlgorithm.GAUSSIAN, "Gaussian Blur"),
        (BlurAlgorithm.MOTION, "Motion Blur"),
    ]
    
    print(f"Testing with {img.size[0]}x{img.size[1]} image:")
    
    for algorithm, name in algorithms:
        start_time = time.time()
        result = apply_progressive_blur(
            img,
            max_blur=30.0,
            algorithm=algorithm
        )
        processing_time = time.time() - start_time
        print(f"  {name}: {processing_time:.2f}s")


def demo_web_optimization():
    """Demonstrate web optimization features."""
    print("\n🌐 Web Optimization Demo")
    print("-" * 50)
    
    # Create a large image
    img = create_sample_image((3000, 2000))
    output_dir = Path("output/web_optimization")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Original size: {img.size}")
    
    # Apply blur and optimize for web
    blurred = apply_progressive_blur(img, max_blur=40.0)
    optimized = optimize_image_for_web(blurred, max_width=1920, max_height=1080)
    
    print(f"Optimized size: {optimized.size}")
    
    # Save with different quality settings
    qualities = [95, 85, 75]
    for quality in qualities:
        optimized.save(
            output_dir / f"optimized_q{quality}.jpg",
            quality=quality,
            optimize=True
        )
        file_size = (output_dir / f"optimized_q{quality}.jpg").stat().st_size
        print(f"  Quality {quality}: {file_size / 1024:.1f} KB")


def demo_alpha_channel():
    """Demonstrate alpha channel preservation."""
    print("\n🔍 Alpha Channel Demo")
    print("-" * 50)
    
    # Create image with transparency
    img = Image.new('RGBA', (600, 400), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw semi-transparent shapes
    draw.ellipse([100, 100, 300, 300], fill=(255, 0, 0, 128))
    draw.rectangle([200, 50, 500, 350], fill=(0, 255, 0, 100))
    
    output_dir = Path("output/alpha_channel")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save original
    img.save(output_dir / "original_alpha.png")
    
    # Apply blur with alpha preservation
    blurred_with_alpha = apply_progressive_blur(img, preserve_alpha=True)
    blurred_with_alpha.save(output_dir / "blurred_with_alpha.png")
    print("✅ Alpha channel preserved")
    
    # Apply blur without alpha preservation
    blurred_without_alpha = apply_progressive_blur(img, preserve_alpha=False)
    blurred_without_alpha.save(output_dir / "blurred_without_alpha.jpg", quality=95)
    print("✅ Alpha channel removed")


def main():
    """Run all demonstration examples."""
    print("🎨 Progressive Blur - Advanced Examples")
    print("=" * 50)
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    
    # Run all demos
    demo_basic_usage()
    demo_directions_and_algorithms()
    demo_easing_functions()
    demo_presets()
    demo_custom_masks()
    demo_batch_processing()
    demo_performance_comparison()
    demo_web_optimization()
    demo_alpha_channel()
    
    print("\n🎉 All examples completed!")
    print("Check the 'output' directory for results.")


if __name__ == "__main__":
    main() 