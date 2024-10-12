# setup.py
from setuptools import setup, find_packages

setup(
    name="cms_model",  # Name of the package
    version="0.1.0",  # Initial version
    description="Coordinated Minima Search: An Efficient Approach for Optimizing Linear and Non-Linear Regression Models.",
    long_description=open('README.md').read(),  # Description from README.md
    long_description_content_type='text/markdown',
    author="Rifat Hassan",
    author_email="h.rifat1609@gmail.com",
    url="https://github.com/RHassan1609/cms.git",  # GitHub repository URL
    packages=find_packages(),  # Automatically find the packages
    license="MIT",  # License type (or any other like Apache 2.0)
    install_requires=[],  # Dependencies for your package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
