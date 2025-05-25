"""
Unit tests for progressive blur core functionality.
"""

import math
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from PIL import Image

from progressive_blur.core import (
    BlurDirection,
    BlurAlgorithm,
    EasingFunction,
    apply_progressive_blur,
    create_custom_blur_mask,
    apply_mask_based_blur,
    _validate_percentage,
    _validate_positive,
    _load_image,
    _apply_easing,
    _create_blur_mask,
    _calculate_blur_intensity,
)


class TestValidationFunctions:
    """Test validation helper functions."""
    
    def test_validate_percentage_valid(self):
        """Test percentage validation with valid values."""
        _validate_percentage(0.0, "test")
        _validate_percentage(0.5, "test")
        _validate_percentage(1.0, "test")
    
    def test_validate_percentage_invalid(self):
        """Test percentage validation with invalid values."""
        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            _validate_percentage(-0.1, "test")
        
        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            _validate_percentage(1.1, "test")
    
    def test_validate_positive_valid(self):
        """Test positive validation with valid values."""
        _validate_positive(0.1, "test")
        _validate_positive(1.0, "test")
        _validate_positive(100.0, "test")
    
    def test_validate_positive_invalid(self):
        """Test positive validation with invalid values."""
        with pytest.raises(ValueError, match="must be positive"):
            _validate_positive(0.0, "test")
        
        with pytest.raises(ValueError, match="must be positive"):
            _validate_positive(-1.0, "test")


class TestImageLoading:
    """Test image loading functionality."""
    
    def test_load_pil_image(self):
        """Test loading PIL Image objects."""
        original = Image.new('RGB', (100, 100), color='red')
        loaded = _load_image(original)
        
        assert loaded.size == original.size
        assert loaded.mode == original.mode
        assert loaded is not original  # Should be a copy
    
    def test_load_from_bytes(self):
        """Test loading images from bytes."""
        # Create a test image and convert to bytes
        img = Image.new('RGB', (50, 50), color='blue')
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img.save(tmp.name)
            with open(tmp.name, 'rb') as f:
                img_bytes = f.read()
        
        loaded = _load_image(img_bytes)
        assert loaded.size == (50, 50)
        assert loaded.mode == 'RGB'
        
        # Cleanup
        Path(tmp.name).unlink()
    
    def test_load_from_file_path(self):
        """Test loading images from file paths."""
        img = Image.new('RGB', (75, 75), color='green')
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            img.save(tmp.name)
            
            loaded = _load_image(tmp.name)
            assert loaded.size == (75, 75)
            
            # Cleanup
            Path(tmp.name).unlink()
    
    def test_load_invalid_type(self):
        """Test loading with invalid input type."""
        with pytest.raises(TypeError, match="Unsupported image input type"):
            _load_image(123)


class TestEasingFunctions:
    """Test easing function implementations."""
    
    def test_linear_easing(self):
        """Test linear easing function."""
        assert _apply_easing(0.0, EasingFunction.LINEAR) == 0.0
        assert _apply_easing(0.5, EasingFunction.LINEAR) == 0.5
        assert _apply_easing(1.0, EasingFunction.LINEAR) == 1.0
    
    def test_ease_in(self):
        """Test ease-in function."""
        assert _apply_easing(0.0, EasingFunction.EASE_IN) == 0.0
        assert _apply_easing(1.0, EasingFunction.EASE_IN) == 1.0
        # Should be slower at the beginning
        assert _apply_easing(0.5, EasingFunction.EASE_IN) < 0.5
    
    def test_ease_out(self):
        """Test ease-out function."""
        assert _apply_easing(0.0, EasingFunction.EASE_OUT) == 0.0
        assert _apply_easing(1.0, EasingFunction.EASE_OUT) == 1.0
        # Should be faster at the beginning
        assert _apply_easing(0.5, EasingFunction.EASE_OUT) > 0.5
    
    def test_ease_in_out(self):
        """Test ease-in-out function."""
        assert _apply_easing(0.0, EasingFunction.EASE_IN_OUT) == 0.0
        assert _apply_easing(1.0, EasingFunction.EASE_IN_OUT) == 1.0
        assert _apply_easing(0.5, EasingFunction.EASE_IN_OUT) == 0.5
    
    def test_exponential_easing(self):
        """Test exponential easing function."""
        assert _apply_easing(0.0, EasingFunction.EXPONENTIAL) == 0.0
        assert _apply_easing(1.0, EasingFunction.EXPONENTIAL) == 1.0
        # Should be much slower at the beginning
        assert _apply_easing(0.5, EasingFunction.EXPONENTIAL) < 0.25
    
    def test_sine_easing(self):
        """Test sine easing function."""
        assert _apply_easing(0.0, EasingFunction.SINE) == 0.0
        assert abs(_apply_easing(1.0, EasingFunction.SINE) - 1.0) < 1e-10
        # Should be approximately sqrt(2)/2 at 0.5
        expected = math.sin(0.5 * math.pi / 2)
        assert abs(_apply_easing(0.5, EasingFunction.SINE) - expected) < 1e-10


class TestBlurIntensityCalculation:
    """Test blur intensity calculation."""
    
    def test_clear_region(self):
        """Test intensity in clear region."""
        intensity = _calculate_blur_intensity(
            0.1, 0.15, 0.25, 0.85, EasingFunction.LINEAR
        )
        assert intensity == 0.0
    
    def test_transition_region(self):
        """Test intensity in transition region."""
        intensity = _calculate_blur_intensity(
            0.2, 0.15, 0.25, 0.85, EasingFunction.LINEAR
        )
        assert 0.0 < intensity < 0.3
    
    def test_progressive_region(self):
        """Test intensity in progressive blur region."""
        intensity = _calculate_blur_intensity(
            0.5, 0.15, 0.25, 0.85, EasingFunction.LINEAR
        )
        assert 0.3 <= intensity <= 1.0
    
    def test_max_blur_region(self):
        """Test intensity in maximum blur region."""
        intensity = _calculate_blur_intensity(
            0.9, 0.15, 0.25, 0.85, EasingFunction.LINEAR
        )
        assert intensity == 1.0


class TestBlurMaskCreation:
    """Test blur mask creation for different directions."""
    
    def test_top_to_bottom_mask(self):
        """Test top-to-bottom blur mask."""
        mask = _create_blur_mask(
            100, 100, BlurDirection.TOP_TO_BOTTOM, 0.1, 0.2, 0.8, EasingFunction.LINEAR
        )
        
        assert mask.shape == (100, 100)
        # Top should be clear
        assert np.all(mask[0, :] == 0.0)
        # Bottom should be blurred
        assert np.all(mask[-1, :] == 1.0)
        # Should be monotonically increasing
        assert mask[10, 0] <= mask[50, 0] <= mask[90, 0]
    
    def test_left_to_right_mask(self):
        """Test left-to-right blur mask."""
        mask = _create_blur_mask(
            100, 100, BlurDirection.LEFT_TO_RIGHT, 0.1, 0.2, 0.8, EasingFunction.LINEAR
        )
        
        assert mask.shape == (100, 100)
        # Left should be clear
        assert np.all(mask[:, 0] == 0.0)
        # Right should be blurred
        assert np.all(mask[:, -1] == 1.0)
    
    def test_center_to_edges_mask(self):
        """Test center-to-edges blur mask."""
        mask = _create_blur_mask(
            100, 100, BlurDirection.CENTER_TO_EDGES, 0.0, 0.1, 0.8, EasingFunction.LINEAR
        )
        
        assert mask.shape == (100, 100)
        # Center should be clearer than edges
        center_intensity = mask[50, 50]
        corner_intensity = mask[0, 0]
        assert center_intensity <= corner_intensity


class TestProgressiveBlur:
    """Test the main progressive blur function."""
    
    def test_basic_blur(self):
        """Test basic progressive blur functionality."""
        img = Image.new('RGB', (100, 100), color='red')
        result = apply_progressive_blur(img)
        
        assert isinstance(result, Image.Image)
        assert result.size == img.size
        assert result.mode == img.mode
    
    def test_different_directions(self):
        """Test blur with different directions."""
        img = Image.new('RGB', (50, 50), color='blue')
        
        for direction in BlurDirection:
            result = apply_progressive_blur(img, direction=direction)
            assert isinstance(result, Image.Image)
            assert result.size == img.size
    
    def test_different_algorithms(self):
        """Test blur with different algorithms."""
        img = Image.new('RGB', (50, 50), color='green')
        
        for algorithm in BlurAlgorithm:
            result = apply_progressive_blur(img, algorithm=algorithm)
            assert isinstance(result, Image.Image)
            assert result.size == img.size
    
    def test_different_easing_functions(self):
        """Test blur with different easing functions."""
        img = Image.new('RGB', (50, 50), color='yellow')
        
        for easing in EasingFunction:
            result = apply_progressive_blur(img, easing=easing)
            assert isinstance(result, Image.Image)
            assert result.size == img.size
    
    def test_alpha_preservation(self):
        """Test alpha channel preservation."""
        img = Image.new('RGBA', (50, 50), color=(255, 0, 0, 128))
        
        # With alpha preservation
        result_with_alpha = apply_progressive_blur(img, preserve_alpha=True)
        assert result_with_alpha.mode == 'RGBA'
        
        # Without alpha preservation
        result_without_alpha = apply_progressive_blur(img, preserve_alpha=False)
        assert result_without_alpha.mode == 'RGB'
    
    def test_parameter_validation(self):
        """Test parameter validation."""
        img = Image.new('RGB', (50, 50), color='white')
        
        # Invalid max_blur
        with pytest.raises(ValueError, match="must be positive"):
            apply_progressive_blur(img, max_blur=0)
        
        # Invalid percentages
        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            apply_progressive_blur(img, clear_until=1.5)
        
        # Invalid parameter relationships
        with pytest.raises(ValueError, match="clear_until must be less than blur_start"):
            apply_progressive_blur(img, clear_until=0.5, blur_start=0.3)
    
    def test_string_enum_conversion(self):
        """Test conversion of string parameters to enums."""
        img = Image.new('RGB', (50, 50), color='black')
        
        result = apply_progressive_blur(
            img,
            direction="left_to_right",
            algorithm="box",
            easing="ease_in"
        )
        
        assert isinstance(result, Image.Image)
        assert result.size == img.size


class TestCustomBlurMask:
    """Test custom blur mask creation."""
    
    def test_custom_mask_creation(self):
        """Test creating custom blur masks."""
        def mask_function(x: int, y: int) -> float:
            # Simple gradient from left to right
            return x / 100.0
        
        mask = create_custom_blur_mask(100, 50, mask_function)
        
        assert mask.shape == (50, 100)
        assert mask[0, 0] == 0.0
        assert mask[0, 99] == 0.99
    
    def test_mask_value_clamping(self):
        """Test that mask values are clamped to [0, 1]."""
        def mask_function(x: int, y: int) -> float:
            return x / 50.0 - 0.5  # Will produce values from -0.5 to 1.5
        
        mask = create_custom_blur_mask(100, 50, mask_function)
        
        assert np.all(mask >= 0.0)
        assert np.all(mask <= 1.0)


class TestMaskBasedBlur:
    """Test mask-based blur functionality."""
    
    def test_mask_based_blur_numpy(self):
        """Test mask-based blur with numpy array mask."""
        img = Image.new('RGB', (50, 50), color='red')
        mask = np.ones((50, 50), dtype=np.float32) * 0.5
        
        result = apply_mask_based_blur(img, mask)
        
        assert isinstance(result, Image.Image)
        assert result.size == img.size
    
    def test_mask_based_blur_pil(self):
        """Test mask-based blur with PIL Image mask."""
        img = Image.new('RGB', (50, 50), color='blue')
        mask_img = Image.new('L', (50, 50), color=128)  # 50% gray
        
        result = apply_mask_based_blur(img, mask_img)
        
        assert isinstance(result, Image.Image)
        assert result.size == img.size
    
    def test_mask_dimension_mismatch(self):
        """Test error handling for mismatched mask dimensions."""
        img = Image.new('RGB', (50, 50), color='green')
        mask = np.ones((30, 30), dtype=np.float32)
        
        with pytest.raises(ValueError, match="Mask dimensions.*don't match"):
            apply_mask_based_blur(img, mask) 