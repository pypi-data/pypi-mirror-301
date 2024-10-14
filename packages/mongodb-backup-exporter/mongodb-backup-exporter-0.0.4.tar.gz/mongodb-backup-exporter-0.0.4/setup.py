import os
import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

# Get version from environment variable or fallback to a default value
version = os.getenv("PACKAGE_VERSION", "0.0.2")  # Default to '0.0.7' if not provided

setuptools.setup(
    name="mongodb-backup-exporter",
    version=version,  # Use the dynamic version from the environment variable
    author="Jorge Cardona",
    description="A tool to export MongoDB collections to JSON or CSV files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorgecardona/mongodb-backup-exporter",
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
