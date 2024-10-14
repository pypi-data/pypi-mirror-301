from setuptools import setup, find_packages

setup(
    name="simple-signature-verify",  # Name of your package
    version="0.1.0",  # Initial version
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[],  # List of dependencies, if any
    author="Adithya K",
    author_email="adithya.k@setu.co",
    description="A Python SDK for verifying HMAC signatures",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
