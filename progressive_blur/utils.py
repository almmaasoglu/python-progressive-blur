"""
Utility functions for progressive blur operations.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple, Union

from PIL import Image

from .core import ImageInput, apply_progressive_blur, BlurDirection, BlurAlgorithm, EasingFunction


def get_supported_formats() -> Tuple[str, ...]:
    """Get tuple of supported image formats."""
    return ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif')


def is_supported_format(file_path: Union[str, Path]) -> bool:
    """Check if a file has a supported image format."""
    return Path(file_path).suffix.lower() in get_supported_formats()


def find_images(
    directory: Union[str, Path], 
    recursive: bool = False
) -> Generator[Path, None, None]:
    """
    Find all supported image files in a directory.
    
    Args:
        directory: Directory to search
        recursive: Whether to search subdirectories
        
    Yields:
        Path: Image file paths
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    pattern = "**/*" if recursive else "*"
    
    for file_path in directory.glob(pattern):
        if file_path.is_file() and is_supported_format(file_path):
            yield file_path


def batch_process_images(
    input_dir: Union[str, Path],
    output_dir: Union[str, Path],
    max_blur: float = 50.0,
    clear_until: float = 0.15,
    blur_start: float = 0.25,
    end_position: float = 0.85,
    direction: Union[BlurDirection, str] = BlurDirection.TOP_TO_BOTTOM,
    algorithm: Union[BlurAlgorithm, str] = BlurAlgorithm.GAUSSIAN,
    easing: Union[EasingFunction, str] = EasingFunction.LINEAR,
    preserve_alpha: bool = True,
    recursive: bool = False,
    overwrite: bool = False,
    quality: int = 95,
    prefix: str = "blurred_",
    progress_callback: Optional[callable] = None,
) -> List[Tuple[Path, Path]]:
    """
    Process multiple images with progressive blur effect.
    
    Args:
        input_dir: Input directory containing images
        output_dir: Output directory for processed images
        max_blur: Maximum blur radius
        clear_until: Percentage to keep completely clear
        blur_start: Percentage where blur starts to appear
        end_position: Percentage where maximum blur is reached
        direction: Direction of the blur effect
        algorithm: Blur algorithm to use
        easing: Easing function for blur transition
        preserve_alpha: Whether to preserve alpha channel
        recursive: Whether to search subdirectories
        overwrite: Whether to overwrite existing files
        quality: JPEG quality (1-100)
        prefix: Prefix for output filenames
        progress_callback: Optional callback function for progress updates
        
    Returns:
        List of (input_path, output_path) tuples for processed files
        
    Raises:
        FileNotFoundError: If input directory doesn't exist
        ValueError: If quality is not in valid range
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    if not 1 <= quality <= 100:
        raise ValueError(f"Quality must be between 1 and 100, got {quality}")
    
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all images
    image_files = list(find_images(input_dir, recursive=recursive))
    processed_files = []
    
    for i, input_path in enumerate(image_files):
        try:
            # Generate output path
            output_filename = f"{prefix}{input_path.name}"
            if recursive:
                # Preserve directory structure
                relative_path = input_path.relative_to(input_dir)
                output_path = output_dir / relative_path.parent / output_filename
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_path = output_dir / output_filename
            
            # Skip if file exists and overwrite is False
            if output_path.exists() and not overwrite:
                continue
            
            # Process image
            blurred_image = apply_progressive_blur(
                str(input_path),
                max_blur=max_blur,
                clear_until=clear_until,
                blur_start=blur_start,
                end_position=end_position,
                direction=direction,
                algorithm=algorithm,
                easing=easing,
                preserve_alpha=preserve_alpha,
            )
            
            # Save with appropriate format and quality
            save_kwargs = {}
            if output_path.suffix.lower() in ('.jpg', '.jpeg'):
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True
            elif output_path.suffix.lower() == '.webp':
                save_kwargs['quality'] = quality
                save_kwargs['method'] = 6  # Better compression
            elif output_path.suffix.lower() == '.png':
                save_kwargs['optimize'] = True
            
            blurred_image.save(output_path, **save_kwargs)
            processed_files.append((input_path, output_path))
            
            # Call progress callback if provided
            if progress_callback:
                progress_callback(i + 1, len(image_files), input_path, output_path)
                
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            continue
    
    return processed_files


def create_blur_preset(
    name: str,
    max_blur: float,
    clear_until: float,
    blur_start: float,
    end_position: float,
    direction: Union[BlurDirection, str] = BlurDirection.TOP_TO_BOTTOM,
    algorithm: Union[BlurAlgorithm, str] = BlurAlgorithm.GAUSSIAN,
    easing: Union[EasingFunction, str] = EasingFunction.LINEAR,
) -> Dict[str, any]:
    """
    Create a blur preset configuration.
    
    Args:
        name: Preset name
        max_blur: Maximum blur radius
        clear_until: Percentage to keep completely clear
        blur_start: Percentage where blur starts to appear
        end_position: Percentage where maximum blur is reached
        direction: Direction of the blur effect
        algorithm: Blur algorithm to use
        easing: Easing function for blur transition
        
    Returns:
        Dictionary containing preset configuration
    """
    return {
        'name': name,
        'max_blur': max_blur,
        'clear_until': clear_until,
        'blur_start': blur_start,
        'end_position': end_position,
        'direction': direction,
        'algorithm': algorithm,
        'easing': easing,
    }


# Predefined presets
BLUR_PRESETS = {
    'subtle': create_blur_preset(
        'Subtle Blur',
        max_blur=20.0,
        clear_until=0.2,
        blur_start=0.3,
        end_position=0.9,
        easing=EasingFunction.EASE_OUT,
    ),
    'dramatic': create_blur_preset(
        'Dramatic Blur',
        max_blur=80.0,
        clear_until=0.1,
        blur_start=0.2,
        end_position=0.7,
        easing=EasingFunction.EASE_IN,
    ),
    'center_focus': create_blur_preset(
        'Center Focus',
        max_blur=60.0,
        clear_until=0.0,
        blur_start=0.1,
        end_position=0.8,
        direction=BlurDirection.EDGES_TO_CENTER,
        easing=EasingFunction.EASE_IN_OUT,
    ),
    'horizontal_fade': create_blur_preset(
        'Horizontal Fade',
        max_blur=40.0,
        clear_until=0.15,
        blur_start=0.25,
        end_position=0.85,
        direction=BlurDirection.LEFT_TO_RIGHT,
        easing=EasingFunction.SINE,
    ),
    'motion_blur': create_blur_preset(
        'Motion Blur Effect',
        max_blur=30.0,
        clear_until=0.1,
        blur_start=0.2,
        end_position=0.8,
        algorithm=BlurAlgorithm.MOTION,
        easing=EasingFunction.LINEAR,
    ),
}


def apply_preset(
    image: ImageInput,
    preset_name: str,
    preserve_alpha: bool = True,
) -> Image.Image:
    """
    Apply a predefined blur preset to an image.
    
    Args:
        image: Input image
        preset_name: Name of the preset to apply
        preserve_alpha: Whether to preserve alpha channel
        
    Returns:
        PIL.Image: Processed image
        
    Raises:
        ValueError: If preset name is not found
    """
    if preset_name not in BLUR_PRESETS:
        available_presets = ', '.join(BLUR_PRESETS.keys())
        raise ValueError(
            f"Unknown preset '{preset_name}'. Available presets: {available_presets}"
        )
    
    preset = BLUR_PRESETS[preset_name]
    
    return apply_progressive_blur(
        image,
        max_blur=preset['max_blur'],
        clear_until=preset['clear_until'],
        blur_start=preset['blur_start'],
        end_position=preset['end_position'],
        direction=preset['direction'],
        algorithm=preset['algorithm'],
        easing=preset['easing'],
        preserve_alpha=preserve_alpha,
    )


def get_image_info(image_path: Union[str, Path]) -> Dict[str, any]:
    """
    Get information about an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing image information
    """
    image_path = Path(image_path)
    
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    with Image.open(image_path) as img:
        return {
            'filename': image_path.name,
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'width': img.width,
            'height': img.height,
            'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info,
            'file_size': image_path.stat().st_size,
        }


def optimize_image_for_web(
    image: Image.Image,
    max_width: int = 1920,
    max_height: int = 1080,
    quality: int = 85,
) -> Image.Image:
    """
    Optimize an image for web use by resizing and compressing.
    
    Args:
        image: Input image
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100)
        
    Returns:
        PIL.Image: Optimized image
    """
    # Calculate new size while maintaining aspect ratio
    width, height = image.size
    
    if width > max_width or height > max_height:
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return image 