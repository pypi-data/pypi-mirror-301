# setup.py

from setuptools import setup, find_packages

setup(
    name="pro-logging",
    version="1.0.0",
    packages=find_packages(),
    description="An advanced logging package for Python projects",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mohamadjavad Heydarpanah',
    author_email='mjavad.heydarpanah@gmail.com',
    url='https://github.com/mjavadhe/arduinopy',
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
