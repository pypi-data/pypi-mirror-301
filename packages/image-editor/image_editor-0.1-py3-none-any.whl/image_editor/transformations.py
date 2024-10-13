from PIL import Image

def flip_horizontal(image):
    """Flip the image horizontally."""
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def flip_vertical(image):
    """Flip the image vertically."""
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def skew(image, skew_factor=0.5):
    """Apply skew transformation to the image."""
    # This function requires more complex math, using affine transformation.
    width, height = image.size
    x_shift = abs(skew_factor) * width
    new_width = width + int(round(x_shift))

    image = image.transform(
        (new_width, height),
        Image.AFFINE,
        (1, skew_factor, -x_shift if skew_factor > 0 else 0, 0, 1, 0),
        Image.BICUBIC)
    
    return image