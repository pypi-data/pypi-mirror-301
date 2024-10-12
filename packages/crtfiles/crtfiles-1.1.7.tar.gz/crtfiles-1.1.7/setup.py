# setup.py
from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "crtfiles"
setup(
    name=NAME,
    version='1.1.7',
    author="feed619",
    author_email="azimovpro@gmail.com",
    description="create files quickly and conveniently with the 'crt' utility",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/feed619/crtfiles",
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'crt=crt.cli:main',
        ],
    },
    license='MIT',
    include_package_data=True,
    package_data={
        'crt': ['data/templates.json', 'data/file_code.json'],
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
)
