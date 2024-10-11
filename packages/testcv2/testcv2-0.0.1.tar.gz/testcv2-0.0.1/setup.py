# setup.py
from setuptools import setup, find_packages

setup(
    name="testcv2",  # This is the name of your package
    version="0.0.1",  # Initial version
    packages=find_packages(),  # Automatically finds the `cv2` package
    description="Compute Vector",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/geoffreyvd/cv2",  # URL to your repo or package page
)