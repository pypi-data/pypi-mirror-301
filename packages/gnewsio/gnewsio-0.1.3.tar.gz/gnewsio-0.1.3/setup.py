from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gnewsio",  # Package name
    version="0.1.3",
    description="A Python client for the GNews API with category, country, and language filtering",
    author="Sanket Mishra",
    author_email="isanketmishra@gmail.com",
    url="https://github.com/project-arth-tech/gnewsio",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    long_description=long_description,
    long_description_content_type="text/markdown",
)