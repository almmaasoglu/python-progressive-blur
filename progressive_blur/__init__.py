"""
Progressive Blur - A high-quality Python library for applying progressive blur effects to images.

This library provides advanced progressive blur functionality with multiple algorithms,
directions, easing functions, and batch processing capabilities.
"""

from .core import (
    BlurDirection,
    BlurAlgorithm,
    EasingFunction,
    apply_progressive_blur,
    create_custom_blur_mask,
    apply_mask_based_blur,
)
from .utils import (
    batch_process_images,
    apply_preset,
    BLUR_PRESETS,
    get_image_info,
    optimize_image_for_web,
    get_supported_formats,
    is_supported_format,
    find_images,
)

# Legacy import for backward compatibility
from .core import apply_progressive_blur as apply_progressive_blur_legacy

__version__ = "1.0.0"
__author__ = "Ali Maasoglu"
__email__ = "ali@example.com"
__description__ = "A high-quality Python library for applying progressive blur effects to images"

__all__ = [
    # Core functionality
    "apply_progressive_blur",
    "create_custom_blur_mask",
    "apply_mask_based_blur",
    
    # Enums
    "BlurDirection",
    "BlurAlgorithm", 
    "EasingFunction",
    
    # Utility functions
    "batch_process_images",
    "apply_preset",
    "get_image_info",
    "optimize_image_for_web",
    "get_supported_formats",
    "is_supported_format",
    "find_images",
    
    # Presets
    "BLUR_PRESETS",
    
    # Legacy compatibility
    "apply_progressive_blur_legacy",
    
    # Package metadata
    "__version__",
    "__author__",
    "__email__",
    "__description__",
]
