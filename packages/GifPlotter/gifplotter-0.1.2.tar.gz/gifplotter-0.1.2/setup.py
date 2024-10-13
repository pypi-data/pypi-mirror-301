from setuptools import setup, find_packages

setup(
    name="GifPlotter",
    version="0.1.2",
    author="Amin Atashnezhad",
    author_email="atashnezhad1@gmail.com",
    description="A library to create and arrange plots and generate GIFs.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/GifPlotter",  # Update with your GitHub URL
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "pandas",
        "imageio"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
