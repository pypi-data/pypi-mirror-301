from setuptools import setup, find_packages
import os

# Dynamic version from the environment variable
version = os.getenv('PACKAGE_VERSION', '0.0.1')

# Long description from README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mongodb-backup-exporter",
    version=version,  # Use the dynamic version from the environment variable
    author="Jorge Cardona",
    description="A tool to export MongoDB collections to JSON or CSV files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorgecardona/mongodb-backup-exporter",
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pymongo==4.10.1',  # Include pymongo to be installed automatically
    ],
)