from setuptools import setup, find_packages

setup(
    name="Gowtham_STT",
    version="1.1.1",
    packages=find_packages(),
    include_package_data=True,  # Ensure non-Python files are included
    install_requires=[
        'selenium',
        'webdriver_manager',
    ],  # List your package dependencies here
    author="Gowtham",
    description="A Speech To Text By Gowtham with HTML, CSS, JS, and Python files",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
