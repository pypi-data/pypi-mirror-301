# Image Editor Library

The **`image-editor`** library is a simple yet powerful Python package for editing images with various drawing tools and effects. Built on top of the popular Pillow library, this library allows you to perform a wide range of image manipulations, including adding strokes, shapes, text, and applying filters.

## Features

- Draw strokes, rectangles, and ellipses.
- Add text with customizable font size and color.
- Apply effects like blur, grayscale, sepia, and sharpen.
- Resize, rotate, and flip images.
- Save edited images in various formats.

## Installation

You can easily install the **`image-editor`** library via pip:

```bash
pip install image-editor
```

## Usage

Here's a quick example of how to use the **`image-editor`** library:

```python
import image_editor as editor

# Load the image using the DrawingImg class
image = editor.load('img.png')

# Perform operations using the class methods
image.stroke(10, 10, 200, 200, width='5px', style='fountain pen')\
     .rectangle(50, 50, 150, 150, outline='red', fill='blue')\
     .add_text("Hello World", (100, 100), font_size=30, color='white')\
     .blur(radius=5)\
     .save('edited_image.png')
```

## Documentation

For more detailed usage and API references, please refer to the [documentation](https://your-documentation-link.com).

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please create an issue or submit a pull request.

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Push to the branch
6. Create a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This library is built on top of the [Pillow](https://python-pillow.org/) library for image processing.