from setuptools import setup,find_packages

setup(
    name='Gowtham_STT',
    version='1.0.0',
    author = 'Gowtham',
    description='A simple speech-to-text application using Google Cloud Speech API.',)
packages= find_packages(),
install_reqirements = [
    'selenium',
    'webdriver_manager'

]