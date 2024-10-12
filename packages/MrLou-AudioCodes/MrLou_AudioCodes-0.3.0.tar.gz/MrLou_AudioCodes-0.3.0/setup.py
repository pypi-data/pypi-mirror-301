from setuptools import setup, find_packages

# Read the content of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="MrLou_AudioCodes",  # Replace with your own package name
    version="0.3.0",  # Initial release version
    author="Louis-Philippe Descamps",  # Replace with your name
    author_email="me@lpdne.eu",  # Replace with your email
    description="A module for MrLou_AudioCodes API",  # Short description
    long_description=long_description,  # Load long description from README.md
    long_description_content_type="text/markdown",  # Set the long description format
    url="https://github.com/lpdescamps/AudioCodes",  # Replace with your GitHub repository
    packages=find_packages(),  # Automatically find all packages in the project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # If you use the MIT License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python version compatibility
    install_requires=[],  # List any dependencies your package needs
)
