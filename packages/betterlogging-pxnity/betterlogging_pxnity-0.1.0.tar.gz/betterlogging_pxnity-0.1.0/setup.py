from setuptools import setup, find_packages
import os

setup(
    name="betterlogging-pxnity",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",
    ],
    entry_points={
        'console_scripts': [
            'betterlogging=main:main',  # Adjust this line to point to your main entry function
        ],
    },
    package_data={
        '': ['config/logging_config.json'],
    },
    include_package_data=True,
    author="Parthiv Pal",
    author_email="parthiv.pal.theheritageschool@gmail.com",
    description="A custom logging package with color support",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.MD')).read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/betterlogging",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)