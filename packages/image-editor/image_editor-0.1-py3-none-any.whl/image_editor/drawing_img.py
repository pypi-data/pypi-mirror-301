from PIL import Image, ImageDraw, ImageFont, ImageFilter

class DrawingImg:
    def __init__(self, image_path):
        """Load an image from the specified file path."""
        self.image = Image.open(image_path)

    def save(self, path):
        """Save the image to the given file path."""
        self.image.save(path)

    def resize(self, width, height):
        """Resize the image to the specified width and height."""
        self.image = self.image.resize((width, height))
        return self

    def rotate(self, degrees):
        """Rotate the image by the given degree."""
        self.image = self.image.rotate(degrees, expand=True)
        return self

    def stroke(self, x1, y1, x2, y2, width='3px', style='fountain pen'):
        """Draw a stroke on the image from (x1, y1) to (x2, y2)."""
        draw = ImageDraw.Draw(self.image)
        pen_width = int(width.replace('px', ''))

        # Handle different stroke styles
        if style == 'fountain pen':
            draw.line([x1, y1, x2, y2], fill="black", width=pen_width)
        elif style == 'brush':
            draw.line([x1, y1, x2, y2], fill="darkgray", width=pen_width * 2)
        else:
            draw.line([x1, y1, x2, y2], fill="black", width=pen_width)
        return self

    def rectangle(self, x1, y1, x2, y2, outline='black', fill=None):
        """Draw a rectangle on the image."""
        draw = ImageDraw.Draw(self.image)
        draw.rectangle([x1, y1, x2, y2], outline=outline, fill=fill)
        return self

    def ellipse(self, x1, y1, x2, y2, outline='black', fill=None):
        """Draw an ellipse on the image."""
        draw = ImageDraw.Draw(self.image)
        draw.ellipse([x1, y1, x2, y2], outline=outline, fill=fill)
        return self

    def add_text(self, text, position, font_path=None, font_size=20, color="black"):
        """Add text to the image at the specified position."""
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        draw.text(position, text, font=font, fill=color)
        return self

    def blur(self, radius=2):
        """Apply a blur effect to the image."""
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
        return self

    def sharpen(self):
        """Sharpen the image."""
        self.image = self.image.filter(ImageFilter.SHARPEN)
        return self

    def grayscale(self):
        """Convert the image to grayscale."""
        self.image = self.image.convert("L")
        return self

    def sepia(self):
        """Convert the image to sepia tone."""
        width, height = self.image.size
        pixels = self.image.load()

        for py in range(height):
            for px in range(width):
                r, g, b = self.image.getpixel((px, py))

                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                tr = min(255, tr)
                tg = min(255, tg)
                tb = min(255, tb)

                pixels[px, py] = (tr, tg, tb)
        return self

    def flip_horizontal(self):
        """Flip the image horizontally."""
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        return self

    def flip_vertical(self):
        """Flip the image vertically."""
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        return self

    def skew(self, skew_factor=0.5):
        """Apply skew transformation to the image."""
        width, height = self.image.size
        x_shift = abs(skew_factor) * width
        new_width = width + int(round(x_shift))

        self.image = self.image.transform(
            (new_width, height),
            Image.AFFINE,
            (1, skew_factor, -x_shift if skew_factor > 0 else 0, 0, 1, 0),
            Image.BICUBIC)
        return self