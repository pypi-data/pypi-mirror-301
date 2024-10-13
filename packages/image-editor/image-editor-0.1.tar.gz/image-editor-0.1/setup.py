from setuptools import setup, find_packages

setup(
    name='image-editor',
    version='0.1',
    description='A simple image editing library with drawing tools and effects',
    author='Aiden Metcalfe',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown"
)