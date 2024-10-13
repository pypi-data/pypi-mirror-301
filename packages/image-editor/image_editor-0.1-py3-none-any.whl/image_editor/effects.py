from PIL import ImageFilter

def blur(image, radius=2):
    """Apply a blur effect to the image."""
    return image.filter(ImageFilter.GaussianBlur(radius))

def sharpen(image):
    """Sharpen the image."""
    return image.filter(ImageFilter.SHARPEN)

def grayscale(image):
    """Convert the image to grayscale."""
    return image.convert("L")

def sepia(image):
    """Convert the image to sepia tone."""
    width, height = image.size
    pixels = image.load()  # Get pixel data
    
    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            # Clip values to fit within RGB range
            tr = min(255, tr)
            tg = min(255, tg)
            tb = min(255, tb)

            pixels[px, py] = (tr, tg, tb)

    return image