from setuptools import setup, find_packages
import r2t

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="r2t",
    version=r2t.__version__,  # Use the version from __init__.py
    description="A tool to combine multiple files from a directory and its subdirectories into a single output file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "chardet",
    ],
    entry_points={
        "console_scripts": [
            "r2t=r2t.r2t:main",
        ],
    },
    include_package_data=True,  # Include non-Python files
)
