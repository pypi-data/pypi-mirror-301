from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="thumbtrail",
    version="1.0.0",
    author="Sariya Ansari",
    description="A tool for generating WebVTT files and thumbnails for video scrubbing with encryption and decryption support.",
    long_description=long_description,  # This will appear on PyPI project page
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/thumbtrail",  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "opencv-python>=4.10.0.84",
        "Pillow>=10.4.0",
        "pycryptodome>=3.21.0",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "thumbtrail=thumbtrail.cli:main",  # CLI entry point
        ],
    },
)
