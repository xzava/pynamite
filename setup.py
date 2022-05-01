#!/usr/bin/env python3

import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(name='pynamite',
      version='0.0.1',
      description='You like dynamodb? But not the boto3 interface? You will love pynamite!',
      author='Mike Hall - Kaurifund.com',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages = ['pynamite'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
      ],
      install_requires=['boto3'],
      python_requires='>=3.8',
      extras_require={
        'gpu': ["pyopencl", "six"],
        'testing': [
            "pytest",
            "torch",
            "tqdm",
        ],
      },
      include_package_data=True)