from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="progressive-blur",
    version="0.1.0",
    author="Alim Maasoglu",
    description="A Python library for applying progressive blur effects to images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/almmaasoglu/python-progressive-blur",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Pillow>=8.0.0",
        "numpy>=1.19.0",
    ],
)
