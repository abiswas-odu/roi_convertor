"""Setuptools magic to install MetaBGC."""
import os
from setuptools import setup, find_packages

install_requires = [
    'click',
    'csbdeep',
    'opencv-python',
    'tifffile',
    'pyklb @ git+https://github.com/bhoeckendorf/pyklb.git@skbuild'
]

def read_version():
    """Read the version from the appropriate place in the library."""
    for line in open(os.path.join("src","roi_convertor",'__main__.py'), 'r'):
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip('"')

setup(
    name="roi_convertor",
    python_requires='>=3.7',
    version=read_version(),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author='Posfai lab development team.',
    author_email='ab50@princeton.edu',
    description='Perform ROI conversion.',
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': ['roi_convert=roi_convertor.__main__:main'],
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