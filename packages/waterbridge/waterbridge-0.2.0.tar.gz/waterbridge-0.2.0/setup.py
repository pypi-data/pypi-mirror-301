from setuptools import setup, find_packages


setup(
    name='waterbridge',  # Package name
    version='0.2.0',      # Version
    description='A tool for identifying water bridges and their topology in RNA–protein complexes.',
    long_description=open('README.md').read(),  # Read the README file
    long_description_content_type='text/markdown',
    author='Raman Jangra',
    author_email='raman.compchem@gmail.com',
    url='https://github.com/RamanCompChem/waterbridges',  # Link to the project repository
    packages=find_packages(),  # Automatically find and include all packages
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',   # Specify minimum Python version
    entry_points={
        'console_scripts': [
            'waterbridge=waterbridge.waterbridge:main',  # Command line entry point
        ],
    },
)
