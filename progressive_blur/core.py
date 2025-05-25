"""
Core progressive blur functionality with advanced algorithms and customization options.
"""

from __future__ import annotations

import math
from enum import Enum
from io import BytesIO
from typing import Any, Callable, Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageFilter

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class BlurDirection(Enum):
    """Direction of the progressive blur effect."""
    
    TOP_TO_BOTTOM = "top_to_bottom"
    BOTTOM_TO_TOP = "bottom_to_top"
    LEFT_TO_RIGHT = "left_to_right"
    RIGHT_TO_LEFT = "right_to_left"
    CENTER_TO_EDGES = "center_to_edges"
    EDGES_TO_CENTER = "edges_to_center"


class BlurAlgorithm(Enum):
    """Available blur algorithms."""
    
    GAUSSIAN = "gaussian"
    BOX = "box"
    MOTION = "motion"


class EasingFunction(Enum):
    """Easing functions for blur transition."""
    
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    EXPONENTIAL = "exponential"
    SINE = "sine"


ImageInput = Union[Image.Image, bytes, str]


def _validate_percentage(value: float, name: str) -> None:
    """Validate that a value is a valid percentage (0.0 to 1.0)."""
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")


def _validate_positive(value: float, name: str) -> None:
    """Validate that a value is positive."""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def _load_image(image_input: ImageInput) -> Image.Image:
    """Load an image from various input types."""
    if isinstance(image_input, Image.Image):
        return image_input.copy()
    elif isinstance(image_input, bytes):
        return Image.open(BytesIO(image_input))
    elif isinstance(image_input, str):
        return Image.open(image_input)
    else:
        raise TypeError(
            f"Unsupported image input type: {type(image_input)}. "
            "Expected PIL.Image, bytes, or file path string."
        )


def _apply_easing(progress: float, easing: EasingFunction) -> float:
    """Apply easing function to progress value."""
    if easing == EasingFunction.LINEAR:
        return progress
    elif easing == EasingFunction.EASE_IN:
        return progress * progress
    elif easing == EasingFunction.EASE_OUT:
        return 1 - (1 - progress) * (1 - progress)
    elif easing == EasingFunction.EASE_IN_OUT:
        if progress < 0.5:
            return 2 * progress * progress
        else:
            return 1 - 2 * (1 - progress) * (1 - progress)
    elif easing == EasingFunction.EXPONENTIAL:
        return progress * progress * progress
    elif easing == EasingFunction.SINE:
        return math.sin(progress * math.pi / 2)
    else:
        return progress


def _create_blur_mask(
    width: int,
    height: int,
    direction: BlurDirection,
    clear_until: float,
    blur_start: float,
    end_position: float,
    easing: EasingFunction,
) -> np.ndarray:
    """Create a blur intensity mask based on direction and parameters."""
    mask = np.zeros((height, width), dtype=np.float32)
    
    if direction == BlurDirection.TOP_TO_BOTTOM:
        for y in range(height):
            y_percent = y / height
            intensity = _calculate_blur_intensity(
                y_percent, clear_until, blur_start, end_position, easing
            )
            mask[y, :] = intensity
            
    elif direction == BlurDirection.BOTTOM_TO_TOP:
        for y in range(height):
            y_percent = 1.0 - (y / height)
            intensity = _calculate_blur_intensity(
                y_percent, clear_until, blur_start, end_position, easing
            )
            mask[y, :] = intensity
            
    elif direction == BlurDirection.LEFT_TO_RIGHT:
        for x in range(width):
            x_percent = x / width
            intensity = _calculate_blur_intensity(
                x_percent, clear_until, blur_start, end_position, easing
            )
            mask[:, x] = intensity
            
    elif direction == BlurDirection.RIGHT_TO_LEFT:
        for x in range(width):
            x_percent = 1.0 - (x / width)
            intensity = _calculate_blur_intensity(
                x_percent, clear_until, blur_start, end_position, easing
            )
            mask[:, x] = intensity
            
    elif direction == BlurDirection.CENTER_TO_EDGES:
        center_x, center_y = width // 2, height // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(height):
            for x in range(width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                distance_percent = distance / max_distance
                intensity = _calculate_blur_intensity(
                    distance_percent, clear_until, blur_start, end_position, easing
                )
                mask[y, x] = intensity
                
    elif direction == BlurDirection.EDGES_TO_CENTER:
        center_x, center_y = width // 2, height // 2
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(height):
            for x in range(width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                distance_percent = 1.0 - (distance / max_distance)
                intensity = _calculate_blur_intensity(
                    distance_percent, clear_until, blur_start, end_position, easing
                )
                mask[y, x] = intensity
    
    return mask


def _calculate_blur_intensity(
    position: float,
    clear_until: float,
    blur_start: float,
    end_position: float,
    easing: EasingFunction,
) -> float:
    """Calculate blur intensity at a given position."""
    if position < clear_until:
        return 0.0
    elif position < blur_start:
        # Smooth transition from clear to blur
        progress = (position - clear_until) / (blur_start - clear_until)
        eased_progress = _apply_easing(progress, easing)
        return 0.3 * eased_progress
    elif position > end_position:
        return 1.0
    else:
        # Progressive blur intensity
        progress = (position - blur_start) / (end_position - blur_start)
        eased_progress = _apply_easing(progress, easing)
        return 0.3 + (0.7 * eased_progress)


def _apply_blur_algorithm(
    image: Image.Image, 
    radius: float, 
    algorithm: BlurAlgorithm
) -> Image.Image:
    """Apply the specified blur algorithm to an image."""
    if algorithm == BlurAlgorithm.GAUSSIAN:
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
    elif algorithm == BlurAlgorithm.BOX:
        return image.filter(ImageFilter.BoxBlur(radius=radius))
    elif algorithm == BlurAlgorithm.MOTION:
        # Motion blur is approximated using multiple directional blurs
        blurred = image
        for angle in [0, 45, 90, 135]:
            kernel_size = max(1, int(radius))
            if kernel_size > 1:
                blurred = blurred.filter(ImageFilter.BoxBlur(radius=radius/4))
        return blurred
    else:
        raise ValueError(f"Unsupported blur algorithm: {algorithm}")


def apply_progressive_blur(
    image: ImageInput,
    max_blur: float = 50.0,
    clear_until: float = 0.15,
    blur_start: float = 0.25,
    end_position: float = 0.85,
    direction: Union[BlurDirection, str] = BlurDirection.TOP_TO_BOTTOM,
    algorithm: Union[BlurAlgorithm, str] = BlurAlgorithm.GAUSSIAN,
    easing: Union[EasingFunction, str] = EasingFunction.LINEAR,
    preserve_alpha: bool = True,
) -> Image.Image:
    """
    Apply a progressive blur effect to an image with advanced customization options.
    
    Args:
        image: Input image (PIL.Image, bytes, or file path)
        max_blur: Maximum blur radius (default: 50.0)
        clear_until: Percentage to keep completely clear (default: 0.15)
        blur_start: Percentage where blur starts to appear (default: 0.25)
        end_position: Percentage where maximum blur is reached (default: 0.85)
        direction: Direction of the blur effect (default: TOP_TO_BOTTOM)
        algorithm: Blur algorithm to use (default: GAUSSIAN)
        easing: Easing function for blur transition (default: LINEAR)
        preserve_alpha: Whether to preserve alpha channel (default: True)
    
    Returns:
        PIL.Image: The processed image with progressive blur effect
        
    Raises:
        ValueError: If parameters are out of valid range
        TypeError: If image input type is not supported
    """
    # Validate parameters
    _validate_positive(max_blur, "max_blur")
    _validate_percentage(clear_until, "clear_until")
    _validate_percentage(blur_start, "blur_start")
    _validate_percentage(end_position, "end_position")
    
    if clear_until >= blur_start:
        raise ValueError("clear_until must be less than blur_start")
    if blur_start >= end_position:
        raise ValueError("blur_start must be less than end_position")
    
    # Convert string enums to enum objects
    if isinstance(direction, str):
        direction = BlurDirection(direction)
    if isinstance(algorithm, str):
        algorithm = BlurAlgorithm(algorithm)
    if isinstance(easing, str):
        easing = EasingFunction(easing)
    
    # Load and prepare image
    img = _load_image(image)
    width, height = img.size
    
    # Handle alpha channel
    has_alpha = img.mode in ('RGBA', 'LA')
    alpha_channel = None
    if has_alpha and preserve_alpha:
        alpha_channel = img.split()[-1]
        img = img.convert('RGB')
    elif has_alpha and not preserve_alpha:
        img = img.convert('RGB')
    
    # Create blur mask
    blur_mask = _create_blur_mask(
        width, height, direction, clear_until, blur_start, end_position, easing
    )
    
    # Create maximally blurred version
    blurred_img = _apply_blur_algorithm(img, max_blur, algorithm)
    
    # Apply progressive blur using the mask
    img_array = np.array(img, dtype=np.float32)
    blurred_array = np.array(blurred_img, dtype=np.float32)
    
    # Expand mask to match image channels
    if len(img_array.shape) == 3:
        blur_mask = np.expand_dims(blur_mask, axis=2)
        blur_mask = np.repeat(blur_mask, img_array.shape[2], axis=2)
    
    # Blend images based on mask
    result_array = img_array * (1 - blur_mask) + blurred_array * blur_mask
    result_array = np.clip(result_array, 0, 255).astype(np.uint8)
    
    # Convert back to PIL Image
    result = Image.fromarray(result_array)
    
    # Restore alpha channel if needed
    if has_alpha and preserve_alpha and alpha_channel is not None:
        result = result.convert('RGBA')
        result.putalpha(alpha_channel)
    
    return result


def create_custom_blur_mask(
    width: int,
    height: int,
    mask_function: Callable[[int, int], float],
) -> np.ndarray:
    """
    Create a custom blur mask using a user-defined function.
    
    Args:
        width: Image width
        height: Image height
        mask_function: Function that takes (x, y) coordinates and returns blur intensity (0.0-1.0)
    
    Returns:
        numpy.ndarray: Blur mask array
    """
    mask = np.zeros((height, width), dtype=np.float32)
    
    for y in range(height):
        for x in range(width):
            intensity = mask_function(x, y)
            mask[y, x] = max(0.0, min(1.0, intensity))
    
    return mask


def apply_mask_based_blur(
    image: ImageInput,
    mask: Union[np.ndarray, Image.Image],
    max_blur: float = 50.0,
    algorithm: Union[BlurAlgorithm, str] = BlurAlgorithm.GAUSSIAN,
) -> Image.Image:
    """
    Apply blur to an image using a custom mask.
    
    Args:
        image: Input image
        mask: Blur intensity mask (0.0-1.0 values)
        max_blur: Maximum blur radius
        algorithm: Blur algorithm to use
    
    Returns:
        PIL.Image: Blurred image
    """
    img = _load_image(image)
    
    if isinstance(algorithm, str):
        algorithm = BlurAlgorithm(algorithm)
    
    # Convert mask to numpy array if needed
    if isinstance(mask, Image.Image):
        mask = np.array(mask.convert('L'), dtype=np.float32) / 255.0
    
    # Ensure mask dimensions match image
    if mask.shape[:2] != img.size[::-1]:
        raise ValueError(
            f"Mask dimensions {mask.shape[:2]} don't match image dimensions {img.size[::-1]}"
        )
    
    # Create blurred version
    blurred_img = _apply_blur_algorithm(img, max_blur, algorithm)
    
    # Apply mask-based blending
    img_array = np.array(img, dtype=np.float32)
    blurred_array = np.array(blurred_img, dtype=np.float32)
    
    if len(img_array.shape) == 3:
        mask = np.expand_dims(mask, axis=2)
        mask = np.repeat(mask, img_array.shape[2], axis=2)
    
    result_array = img_array * (1 - mask) + blurred_array * mask
    result_array = np.clip(result_array, 0, 255).astype(np.uint8)
    
    return Image.fromarray(result_array) 