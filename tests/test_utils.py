"""
Unit tests for progressive blur utility functions.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from progressive_blur.utils import (
    get_supported_formats,
    is_supported_format,
    find_images,
    batch_process_images,
    create_blur_preset,
    BLUR_PRESETS,
    apply_preset,
    get_image_info,
    optimize_image_for_web,
)
from progressive_blur.core import BlurDirection, BlurAlgorithm, EasingFunction


class TestFormatSupport:
    """Test format support utilities."""
    
    def test_get_supported_formats(self):
        """Test getting supported formats."""
        formats = get_supported_formats()
        assert isinstance(formats, tuple)
        assert '.jpg' in formats
        assert '.png' in formats
        assert '.webp' in formats
    
    def test_is_supported_format_valid(self):
        """Test format validation with valid formats."""
        assert is_supported_format('image.jpg')
        assert is_supported_format('image.PNG')  # Case insensitive
        assert is_supported_format(Path('image.webp'))
    
    def test_is_supported_format_invalid(self):
        """Test format validation with invalid formats."""
        assert not is_supported_format('document.txt')
        assert not is_supported_format('video.mp4')
        assert not is_supported_format('image')  # No extension


class TestImageDiscovery:
    """Test image discovery functionality."""
    
    def test_find_images_basic(self):
        """Test basic image finding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create test images
            img = Image.new('RGB', (10, 10), color='red')
            (tmpdir / 'test1.jpg').touch()
            (tmpdir / 'test2.png').touch()
            (tmpdir / 'document.txt').touch()  # Should be ignored
            
            images = list(find_images(tmpdir))
            image_names = [img.name for img in images]
            
            assert 'test1.jpg' in image_names
            assert 'test2.png' in image_names
            assert 'document.txt' not in image_names
    
    def test_find_images_recursive(self):
        """Test recursive image finding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create nested structure
            subdir = tmpdir / 'subdir'
            subdir.mkdir()
            
            (tmpdir / 'root.jpg').touch()
            (subdir / 'nested.png').touch()
            
            # Non-recursive
            images_non_recursive = list(find_images(tmpdir, recursive=False))
            assert len(images_non_recursive) == 1
            assert images_non_recursive[0].name == 'root.jpg'
            
            # Recursive
            images_recursive = list(find_images(tmpdir, recursive=True))
            assert len(images_recursive) == 2
            image_names = [img.name for img in images_recursive]
            assert 'root.jpg' in image_names
            assert 'nested.png' in image_names
    
    def test_find_images_nonexistent_directory(self):
        """Test error handling for nonexistent directory."""
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            list(find_images('/nonexistent/directory'))


class TestBatchProcessing:
    """Test batch processing functionality."""
    
    def test_batch_process_basic(self):
        """Test basic batch processing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / 'input'
            output_dir = Path(tmpdir) / 'output'
            input_dir.mkdir()
            
            # Create test images
            img = Image.new('RGB', (50, 50), color='blue')
            img.save(input_dir / 'test1.jpg')
            img.save(input_dir / 'test2.png')
            
            # Process images
            processed = batch_process_images(
                input_dir,
                output_dir,
                max_blur=10.0,  # Small blur for speed
            )
            
            assert len(processed) == 2
            assert output_dir.exists()
            assert (output_dir / 'blurred_test1.jpg').exists()
            assert (output_dir / 'blurred_test2.png').exists()
    
    def test_batch_process_with_prefix(self):
        """Test batch processing with custom prefix."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / 'input'
            output_dir = Path(tmpdir) / 'output'
            input_dir.mkdir()
            
            img = Image.new('RGB', (30, 30), color='green')
            img.save(input_dir / 'test.jpg')
            
            batch_process_images(
                input_dir,
                output_dir,
                prefix='custom_',
                max_blur=5.0,
            )
            
            assert (output_dir / 'custom_test.jpg').exists()
    
    def test_batch_process_overwrite_protection(self):
        """Test overwrite protection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / 'input'
            output_dir = Path(tmpdir) / 'output'
            input_dir.mkdir()
            output_dir.mkdir()
            
            img = Image.new('RGB', (30, 30), color='red')
            img.save(input_dir / 'test.jpg')
            
            # Create existing output file
            (output_dir / 'blurred_test.jpg').touch()
            
            # Should skip existing file
            processed = batch_process_images(
                input_dir,
                output_dir,
                overwrite=False,
                max_blur=5.0,
            )
            
            assert len(processed) == 0
            
            # Should overwrite with overwrite=True
            processed = batch_process_images(
                input_dir,
                output_dir,
                overwrite=True,
                max_blur=5.0,
            )
            
            assert len(processed) == 1
    
    def test_batch_process_invalid_quality(self):
        """Test error handling for invalid quality."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / 'input'
            output_dir = Path(tmpdir) / 'output'
            
            with pytest.raises(ValueError, match="Quality must be between 1 and 100"):
                batch_process_images(input_dir, output_dir, quality=150)


class TestPresets:
    """Test preset functionality."""
    
    def test_create_blur_preset(self):
        """Test creating custom blur presets."""
        preset = create_blur_preset(
            'test_preset',
            max_blur=25.0,
            clear_until=0.1,
            blur_start=0.2,
            end_position=0.9,
            direction=BlurDirection.LEFT_TO_RIGHT,
        )
        
        assert preset['name'] == 'test_preset'
        assert preset['max_blur'] == 25.0
        assert preset['direction'] == BlurDirection.LEFT_TO_RIGHT
    
    def test_predefined_presets_exist(self):
        """Test that predefined presets exist and are valid."""
        assert 'subtle' in BLUR_PRESETS
        assert 'dramatic' in BLUR_PRESETS
        assert 'center_focus' in BLUR_PRESETS
        
        for preset_name, preset in BLUR_PRESETS.items():
            assert 'name' in preset
            assert 'max_blur' in preset
            assert isinstance(preset['direction'], BlurDirection)
            assert isinstance(preset['algorithm'], BlurAlgorithm)
            assert isinstance(preset['easing'], EasingFunction)
    
    def test_apply_preset_valid(self):
        """Test applying valid presets."""
        img = Image.new('RGB', (50, 50), color='yellow')
        
        for preset_name in BLUR_PRESETS.keys():
            result = apply_preset(img, preset_name)
            assert isinstance(result, Image.Image)
            assert result.size == img.size
    
    def test_apply_preset_invalid(self):
        """Test error handling for invalid preset names."""
        img = Image.new('RGB', (50, 50), color='purple')
        
        with pytest.raises(ValueError, match="Unknown preset"):
            apply_preset(img, 'nonexistent_preset')


class TestImageInfo:
    """Test image information utilities."""
    
    def test_get_image_info_basic(self):
        """Test getting basic image information."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img = Image.new('RGB', (100, 200), color='orange')
            img.save(tmp.name)
            
            info = get_image_info(tmp.name)
            
            assert info['width'] == 100
            assert info['height'] == 200
            assert info['size'] == (100, 200)
            assert info['mode'] == 'RGB'
            assert info['format'] == 'PNG'
            assert not info['has_transparency']
            assert info['file_size'] > 0
            
            Path(tmp.name).unlink()
    
    def test_get_image_info_with_alpha(self):
        """Test getting info for images with transparency."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img = Image.new('RGBA', (50, 50), color=(255, 0, 0, 128))
            img.save(tmp.name)
            
            info = get_image_info(tmp.name)
            
            assert info['mode'] == 'RGBA'
            assert info['has_transparency']
            
            Path(tmp.name).unlink()
    
    def test_get_image_info_nonexistent(self):
        """Test error handling for nonexistent files."""
        with pytest.raises(FileNotFoundError, match="Image file not found"):
            get_image_info('/nonexistent/image.jpg')


class TestImageOptimization:
    """Test image optimization utilities."""
    
    def test_optimize_no_resize_needed(self):
        """Test optimization when no resize is needed."""
        img = Image.new('RGB', (800, 600), color='cyan')
        optimized = optimize_image_for_web(img, max_width=1920, max_height=1080)
        
        assert optimized.size == (800, 600)
    
    def test_optimize_resize_by_width(self):
        """Test optimization when width exceeds limit."""
        img = Image.new('RGB', (2000, 1000), color='magenta')
        optimized = optimize_image_for_web(img, max_width=1920, max_height=1080)
        
        # Should be resized to maintain aspect ratio
        assert optimized.width == 1920
        assert optimized.height == 960  # Maintains 2:1 ratio
    
    def test_optimize_resize_by_height(self):
        """Test optimization when height exceeds limit."""
        img = Image.new('RGB', (1000, 2000), color='lime')
        optimized = optimize_image_for_web(img, max_width=1920, max_height=1080)
        
        # Should be resized to maintain aspect ratio
        assert optimized.width == 540  # Maintains 1:2 ratio
        assert optimized.height == 1080
    
    def test_optimize_resize_both_dimensions(self):
        """Test optimization when both dimensions exceed limits."""
        img = Image.new('RGB', (3000, 2000), color='navy')
        optimized = optimize_image_for_web(img, max_width=1920, max_height=1080)
        
        # Should be resized by the more restrictive dimension
        assert optimized.width == 1620  # Limited by height: 1080 * (3000/2000)
        assert optimized.height == 1080 