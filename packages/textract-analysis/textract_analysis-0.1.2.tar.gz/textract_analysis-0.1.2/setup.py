# setup.py

from setuptools import setup, find_packages

setup(
    name='textract_analysis',
    version='0.1.2',
    description='A package for analyzing ID documents using AWS Textract',
    author='Swarup',
    author_email='swarup.ogma@gmail.com',
    packages=find_packages(),
    install_requires=[
        'boto3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)