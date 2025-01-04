from PIL import Image, ImageFilter
from io import BytesIO
import numpy as np

def apply_progressive_blur(
    image,
    max_blur=50.0,
    clear_until=0.15,
    blur_start=0.25,
    end_y=0.85
):
    """
    Apply a progressive blur effect to an image, creating a smooth transition from clear to blurred areas.
    
    Args:
        image: PIL Image or bytes object containing the image
        max_blur (float): Maximum blur radius (default: 50.0)
        clear_until (float): Percentage of image height to keep completely clear (default: 0.15)
        blur_start (float): Percentage where blur starts to appear (default: 0.25)
        end_y (float): Percentage where maximum blur is reached (default: 0.85)
    
    Returns:
        PIL.Image: The processed image with progressive blur effect
    """
    # Convert image to PIL Image if it's bytes
    if isinstance(image, bytes):
        image = Image.open(BytesIO(image))
    
    # Create base image
    width, height = image.size
    result = image.copy()
    
    # Create a gradient mask for the blur intensity
    mask = Image.new('L', (width, height))
    mask_data = np.array(mask)
    
    # Create the blur intensity gradient
    for y in range(height):
        y_percent = y / height
        if y_percent < clear_until:
            # Completely clear at top
            blur_intensity = 0
        elif y_percent < blur_start:
            # Smooth transition from clear to blur
            progress = (y_percent - clear_until) / (blur_start - clear_until)
            blur_intensity = int(255 * (0.3 * progress))
        elif y_percent > end_y:
            blur_intensity = 255
        else:
            # Calculate progressive blur intensity
            progress = (y_percent - blur_start) / (end_y - blur_start)
            blur_intensity = int(255 * (0.3 + (0.7 * progress)))
        mask_data[y, :] = blur_intensity
    
    # Convert back to PIL Image
    blur_mask = Image.fromarray(mask_data)
    
    # Create maximally blurred version
    blurred = image.filter(ImageFilter.GaussianBlur(radius=max_blur))
    
    # Composite original and blurred images using the gradient mask
    result = Image.composite(blurred, image, blur_mask)
    
    return result
