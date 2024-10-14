from setuptools import setup, find_packages, Command
import os
import shutil

setup(
    name='juicydir',
    version='1.0.7',
    description='Juicy Dir - Recursive File & Content Scanner',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Griffin Skaff',
    author_email='griffts@comcast.net',
    url='https://github.com/TraxionRPh/juicydir',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'juicydir=juicydir.juicydir:main',
        ],
    },
    install_requires=[
        'PyYAML',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)