
from setuptools import setup, find_packages

setup(
    name='ragshu',             # Name of the package
    version='0.1.0',                   # Version of the package
    packages=find_packages(),          # Automatically find packages in the directory
    install_requires=[],               # Dependencies (if any)
    author='Raghav',
    author_email='raghavshukla2010@gmail.com',
    description='A simple math utility library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',                     # License type
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
