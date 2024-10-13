from .drawing_img import DrawingImg

def load(image_path):
    """Return a DrawingImg object after loading the image."""
    return DrawingImg(image_path)