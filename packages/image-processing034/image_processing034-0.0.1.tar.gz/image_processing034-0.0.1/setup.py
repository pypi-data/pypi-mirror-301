from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing034",
    version="0.0.1",
    author="Edyane Araujo",
    description="Image processing package using skimage",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Anne034/image_processing",
    packages=find_packages(),
    install_requires=[
    'scikit-image',  # Por exemplo
    'numpy',
    'pillow',
],
    python_requires='>=3.5',
)