"""Setuptools magic to install MetaBGC."""
import os
from setuptools import setup, find_packages

install_requires = [
    'click',
    'csbdeep',
    'numpy',
    'opencv-python',
    'tifffile'
]

setup(
    name="roi_convertor",
    python_requires='>=3.7',
    version='0.1a',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author='Posfai lab development team.',
    author_email='ab50@princeton.edu',
    description='Perform ROI conversion.',
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': ['roi_convert=src.roi_convertor.__main__:main'],
    },
    url='https://github.com/abiswas-odu/roi_convertor',
    license='GNU General Public License v3',
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
    ]
)