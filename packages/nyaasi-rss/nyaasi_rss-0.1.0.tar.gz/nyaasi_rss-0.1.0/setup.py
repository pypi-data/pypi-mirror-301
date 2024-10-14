from setuptools import setup, find_packages

setup(
    name="nyaasi_rss",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
    ],
    description="A package for fetching and parsing RSS feeds from nyaa.si.",
    author="Praveen",
    author_email="pvnt20@gmail.com",
    url="https://github.com/praveensenpai/nyaasi_rss",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
