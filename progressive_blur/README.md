# Progressive Blur

<div align="center">
  <img src="example_01.jpeg" alt="Example 1" width="400"/>
  <img src="example_02.jpeg" alt="Example 2" width="400"/>
</div>

A Python library that applies a progressive blur effect to images, creating a smooth transition from clear to blurred areas. Perfect for creating visually appealing image effects where you want to gradually blur portions of an image.

## Installation

```bash
pip install progressive-blur
```

Or install from source:
```bash
git clone https://github.com/almmaasoglu/python-progressive-blur.git
cd python-progressive-blur
pip install -e .
```

## Quick Start

```python
from PIL import Image
from progressive_blur import apply_progressive_blur

# Load your image
image = Image.open("your_image.jpg")

# Apply progressive blur with default parameters
blurred_image = apply_progressive_blur(image)

# Or customize the blur effect
custom_blur = apply_progressive_blur(
    image,
    max_blur=50.0,        # Maximum blur radius
    clear_until=0.15,     # Keep top 15% clear
    blur_start=0.25,      # Start blur at 25% from top
    end_y=0.85           # Maximum blur at 85% from top
)

# Save the result
blurred_image.save("blurred_output.jpg")
```

## Features

- Simple and intuitive API
- Customizable blur parameters
- Support for various image formats (JPG, JPEG, PNG, WebP)
- Handles transparent images (RGBA mode)
- Built on reliable image processing libraries (Pillow, NumPy)

## Parameters

The `apply_progressive_blur` function accepts the following parameters:

- `image`: PIL Image or bytes object containing the image
- `max_blur` (float): Maximum blur radius (default: 50.0)
- `clear_until` (float): Percentage of image height to keep completely clear (default: 0.15)
- `blur_start` (float): Percentage where blur starts to appear (default: 0.25)
- `end_y` (float): Percentage where maximum blur is reached (default: 0.85)

## Requirements

- Python 3.6+
- Pillow >= 8.0.0
- NumPy >= 1.19.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.