# Progressive Blur

<div align="center">
  <img src="example_01.jpeg" alt="Example 1" width="400"/>
  <img src="example_02.jpeg" alt="Example 2" width="400"/>
  
  [![PyPI version](https://badge.fury.io/py/progressive-blur.svg)](https://badge.fury.io/py/progressive-blur)
  [![Python Support](https://img.shields.io/pypi/pyversions/progressive-blur.svg)](https://pypi.org/project/progressive-blur/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Tests](https://github.com/almmaasoglu/python-progressive-blur/workflows/tests/badge.svg)](https://github.com/almmaasoglu/python-progressive-blur/actions)
</div>

A **high-quality Python library** for applying progressive blur effects to images. Create stunning visual effects with smooth, customizable blur transitions that can enhance your images with professional-grade results.

## ✨ Features

- 🎯 **Multiple Blur Directions**: Top-to-bottom, left-to-right, center-to-edges, and more
- 🔧 **Advanced Algorithms**: Gaussian, Box, and Motion blur algorithms
- 📈 **Easing Functions**: Linear, ease-in/out, exponential, and sine transitions
- 🎨 **Custom Masks**: Create your own blur patterns with custom functions
- 🚀 **Batch Processing**: Process multiple images efficiently
- 📱 **CLI Tool**: Command-line interface for quick operations
- 🎛️ **Presets**: Ready-to-use blur configurations
- 🔍 **Alpha Channel Support**: Preserve transparency in images
- 📊 **Type Hints**: Full type annotation support
- 🧪 **Comprehensive Tests**: Thoroughly tested codebase

## 🚀 Installation

### From PyPI (Recommended)

```bash
pip install progressive-blur
```

### From Source

```bash
git clone https://github.com/almmaasoglu/python-progressive-blur.git
cd python-progressive-blur
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/almmaasoglu/python-progressive-blur.git
cd python-progressive-blur
pip install -e ".[dev]"
```

## 📖 Quick Start

### Basic Usage

```python
from PIL import Image
from progressive_blur import apply_progressive_blur

# Load your image
image = Image.open("your_image.jpg")

# Apply default progressive blur
blurred = apply_progressive_blur(image)
blurred.save("blurred_image.jpg")
```

### Advanced Usage

```python
from progressive_blur import (
    apply_progressive_blur,
    BlurDirection,
    BlurAlgorithm,
    EasingFunction
)

# Custom blur with advanced options
result = apply_progressive_blur(
    image,
    max_blur=60.0,                    # Maximum blur intensity
    clear_until=0.2,                  # Keep top 20% clear
    blur_start=0.3,                   # Start blur at 30%
    end_position=0.9,                 # Reach max blur at 90%
    direction=BlurDirection.LEFT_TO_RIGHT,
    algorithm=BlurAlgorithm.GAUSSIAN,
    easing=EasingFunction.EASE_IN_OUT,
    preserve_alpha=True
)
```

### Using Presets

```python
from progressive_blur import apply_preset, BLUR_PRESETS

# Apply a predefined preset
dramatic_blur = apply_preset(image, "dramatic")
subtle_blur = apply_preset(image, "subtle")
center_focus = apply_preset(image, "center_focus")

# List available presets
print("Available presets:", list(BLUR_PRESETS.keys()))
```

### Batch Processing

```python
from progressive_blur import batch_process_images

# Process all images in a directory
processed_files = batch_process_images(
    input_dir="./input_images",
    output_dir="./output_images",
    preset="dramatic",
    recursive=True,
    overwrite=False
)

print(f"Processed {len(processed_files)} images")
```

### Custom Blur Masks

```python
from progressive_blur import create_custom_blur_mask, apply_mask_based_blur
import numpy as np

# Create a custom circular blur mask
def circular_mask(x: int, y: int) -> float:
    center_x, center_y = 250, 250  # Image center
    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    max_distance = 200
    return min(1.0, distance / max_distance)

# Apply custom mask
mask = create_custom_blur_mask(500, 500, circular_mask)
result = apply_mask_based_blur(image, mask, max_blur=40.0)
```

## 🖥️ Command Line Interface

The library includes a powerful CLI tool for quick image processing:

### Basic Commands

```bash
# Apply default blur to a single image
progressive-blur input.jpg output.jpg

# Use a preset
progressive-blur input.jpg output.jpg --preset dramatic

# Custom parameters
progressive-blur input.jpg output.jpg --max-blur 30 --direction left_to_right --easing ease_in_out

# Batch process a directory
progressive-blur --batch input_dir/ output_dir/ --preset subtle --recursive

# Get image information
progressive-blur --info image.jpg

# List available presets
progressive-blur --list-presets
```

### Advanced CLI Options

```bash
# Full customization
progressive-blur input.jpg output.jpg \
  --max-blur 45 \
  --clear-until 0.1 \
  --blur-start 0.2 \
  --end-position 0.8 \
  --direction center_to_edges \
  --algorithm gaussian \
  --easing exponential \
  --quality 95
```

## 📚 API Reference

### Core Functions

#### `apply_progressive_blur()`

Apply progressive blur effect to an image.

**Parameters:**
- `image` (ImageInput): Input image (PIL.Image, bytes, or file path)
- `max_blur` (float): Maximum blur radius (default: 50.0)
- `clear_until` (float): Percentage to keep completely clear (default: 0.15)
- `blur_start` (float): Percentage where blur starts (default: 0.25)
- `end_position` (float): Percentage where maximum blur is reached (default: 0.85)
- `direction` (BlurDirection): Direction of blur effect
- `algorithm` (BlurAlgorithm): Blur algorithm to use
- `easing` (EasingFunction): Easing function for transition
- `preserve_alpha` (bool): Whether to preserve alpha channel

**Returns:** `PIL.Image`

### Enums

#### `BlurDirection`
- `TOP_TO_BOTTOM`: Blur from top to bottom
- `BOTTOM_TO_TOP`: Blur from bottom to top
- `LEFT_TO_RIGHT`: Blur from left to right
- `RIGHT_TO_LEFT`: Blur from right to left
- `CENTER_TO_EDGES`: Blur from center outward
- `EDGES_TO_CENTER`: Blur from edges inward

#### `BlurAlgorithm`
- `GAUSSIAN`: Gaussian blur (smooth, natural)
- `BOX`: Box blur (faster, more geometric)
- `MOTION`: Motion blur effect

#### `EasingFunction`
- `LINEAR`: Constant rate of change
- `EASE_IN`: Slow start, fast end
- `EASE_OUT`: Fast start, slow end
- `EASE_IN_OUT`: Slow start and end
- `EXPONENTIAL`: Exponential curve
- `SINE`: Sine wave curve

### Utility Functions

#### `batch_process_images()`
Process multiple images with the same settings.

#### `apply_preset()`
Apply predefined blur configurations.

#### `get_image_info()`
Get detailed information about an image file.

#### `optimize_image_for_web()`
Optimize images for web use with resizing and compression.

## 🎨 Available Presets

| Preset | Description | Max Blur | Direction | Algorithm |
|--------|-------------|----------|-----------|-----------|
| `subtle` | Gentle blur effect | 20.0 | Top to Bottom | Gaussian |
| `dramatic` | Strong blur effect | 80.0 | Top to Bottom | Gaussian |
| `center_focus` | Focus on center | 60.0 | Edges to Center | Gaussian |
| `horizontal_fade` | Left to right fade | 40.0 | Left to Right | Gaussian |
| `motion_blur` | Motion effect | 30.0 | Top to Bottom | Motion |

## 🔧 Advanced Examples

### Creating a Vignette Effect

```python
from progressive_blur import apply_progressive_blur, BlurDirection

vignette = apply_progressive_blur(
    image,
    max_blur=25.0,
    clear_until=0.0,
    blur_start=0.3,
    end_position=1.0,
    direction=BlurDirection.EDGES_TO_CENTER,
    easing="ease_out"
)
```

### Depth of Field Effect

```python
# Simulate camera depth of field
depth_effect = apply_progressive_blur(
    image,
    max_blur=35.0,
    clear_until=0.4,
    blur_start=0.5,
    end_position=0.8,
    direction=BlurDirection.TOP_TO_BOTTOM,
    easing="exponential"
)
```

### Custom Gradient Blur

```python
import numpy as np

def diagonal_gradient(x: int, y: int) -> float:
    """Create a diagonal blur gradient."""
    width, height = 1000, 800  # Your image dimensions
    diagonal_progress = (x / width + y / height) / 2
    return min(1.0, diagonal_progress)

mask = create_custom_blur_mask(1000, 800, diagonal_gradient)
result = apply_mask_based_blur(image, mask, max_blur=50.0)
```

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=progressive_blur --cov-report=html
```

## 📊 Performance

The library is optimized for performance:

- **Vectorized operations** using NumPy for fast mask generation
- **Efficient memory usage** with in-place operations where possible
- **Batch processing** capabilities for handling multiple images
- **Multiple algorithms** to choose speed vs. quality trade-offs

### Benchmarks

| Image Size | Algorithm | Processing Time |
|------------|-----------|-----------------|
| 1920x1080 | Gaussian | ~0.8s |
| 1920x1080 | Box | ~0.4s |
| 4K (3840x2160) | Gaussian | ~2.1s |

*Benchmarks run on MacBook Pro M1, times may vary based on hardware and blur intensity.*

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/almmaasoglu/python-progressive-blur.git
cd python-progressive-blur
pip install -e ".[dev]"
pre-commit install
```

### Running Quality Checks

```bash
# Format code
black progressive_blur tests examples
isort progressive_blur tests examples

# Type checking
mypy progressive_blur

# Linting
flake8 progressive_blur tests
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Pillow](https://pillow.readthedocs.io/) for image processing
- Uses [NumPy](https://numpy.org/) for efficient array operations
- Inspired by modern image editing tools and techniques

## 📞 Support

- 📖 [Documentation](https://github.com/almmaasoglu/python-progressive-blur#readme)
- 🐛 [Issue Tracker](https://github.com/almmaasoglu/python-progressive-blur/issues)
- 💬 [Discussions](https://github.com/almmaasoglu/python-progressive-blur/discussions)

## 🔗 Links

- [PyPI Package](https://pypi.org/project/progressive-blur/)
- [GitHub Repository](https://github.com/almmaasoglu/python-progressive-blur)
- [Change Log](CHANGELOG.md)

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/almmaasoglu">Ali Maasoglu</a>
</div>