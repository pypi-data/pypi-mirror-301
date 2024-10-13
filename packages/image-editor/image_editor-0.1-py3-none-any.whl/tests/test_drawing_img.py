import unittest
import os
import image_editor as editor

class TestDrawingImg(unittest.TestCase):

    def setUp(self):
        """Create an image for testing."""
        self.test_image_path = 'test_image.png'
        self.test_image = editor.load(self.test_image_path)

    def tearDown(self):
        """Remove any test files created."""
        if os.path.exists('output_image.png'):
            os.remove('output_image.png')

    def test_load_and_save(self):
        """Test loading and saving an image."""
        img = self.test_image
        img.save('output_image.png')
        self.assertTrue(os.path.exists('output_image.png'))

    def test_stroke(self):
        """Test drawing a stroke on the image."""
        img = self.test_image
        img.stroke(10, 10, 100, 100).save('output_image.png')
        self.assertTrue(os.path.exists('output_image.png'))

    def test_resize(self):
        """Test resizing the image."""
        img = self.test_image
        img.resize(100, 100).save('output_image.png')
        output_img = editor.load('output_image.png')
        self.assertEqual(output_img.image.size, (100, 100))

    def test_rotate(self):
        """Test rotating the image."""
        img = self.test_image
        img.rotate(90).save('output_image.png')
        output_img = editor.load('output_image.png')
        self.assertEqual(output_img.image.size, (self.test_image.image.size[1], self.test_image.image.size[0]))

    def test_add_text(self):
        """Test adding text to the image."""
        img = self.test_image
        img.add_text("Test", (10, 10), font_size=20).save('output_image.png')
        self.assertTrue(os.path.exists('output_image.png'))

if __name__ == '__main__':
    unittest.main()