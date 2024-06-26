from setuptools import setup, find_packages

# Version : 0.1.0
# Current state : Deprecated
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com


setup(
    name="myBankPackage",
    version="0.1.0",
    author="Guillaume Pot",
    author_email="guillaumepot.pro@outlook.com",
    description="Contains simple tools to create a personal bank app",
    long_description_content_type="text/markdown",
    url="https://github.com/guillaumepot/my_bank_app",
    packages=find_packages(),
    classifiers=[ 
        "Programming Language :: Python :: 3.10.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "pandas",
    ],
    python_requires='>=3.10',
)