from setuptools import setup, find_packages

setup(
    name="simpletestok",              # Name of your package
    version="0.1.0",                  # Initial version number
    author="Maxton Bernal",               # Your name or organization
    author_email="MaxtonBernal@proton.me",
    description="Package used to ping stuff",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # If README is in Markdown
    url="https://github.com/yourusername/your_project",  # Your package's repository
    packages=find_packages(),         # Automatically find packages
    install_requires=[],
    classifiers=[                     # Optional, but recommended for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Change if you use another license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',           # Minimum Python version
)
