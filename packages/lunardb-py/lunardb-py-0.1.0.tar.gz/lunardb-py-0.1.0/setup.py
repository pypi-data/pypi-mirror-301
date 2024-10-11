from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lunardb-py",
    version="0.1.0",
    author="Kazooki123",
    author_email="mgamerdinge146@gmail.com",
    description="A Python SDK for LunarDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kazooki123/lunardb-python-sdk",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
    ],
    extras_require={
        "dev": ["pytest>=6.2.3", "black>=21.5b1", "flake8>=3.9.1"],
    },
)