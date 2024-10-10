from setuptools import setup, find_packages

setup(
    name="arnold-bhadauria",  # The name of your package
    version="0.1.0",  # Initial release version
    description="A simple package to calculate area and perimeter of 2d shapes.",
    long_description=open('README.md').read(),  # The content of your README file
    long_description_content_type="text/markdown",  # The type of the long description
    author="Arnold Bhadauria",
    author_email="arnoldbhadauria8@gmail.com",
    url="",  # URL of your project's repo
    packages=find_packages(),  # Automatically find packages in your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
