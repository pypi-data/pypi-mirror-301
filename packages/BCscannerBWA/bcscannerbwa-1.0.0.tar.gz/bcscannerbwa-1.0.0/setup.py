# -*- coding: utf-8 -*-



import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="BCscannerBWA", 
    version="1.0.0",
    author="Dawn",
    author_email="605547565@qq.com",
    description='Barcode split for Cyclone',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dawangran/BCscannerBWA",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
    
)