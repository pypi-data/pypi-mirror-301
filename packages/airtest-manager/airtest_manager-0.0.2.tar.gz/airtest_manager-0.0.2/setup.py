from setuptools import setup, find_packages

setup(
    name="airtest_manager",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "airtest",
    ],
    author="nibilin33",
    author_email="nibilin33@gmail.com",
    description="support using image url for airtest Template",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/nibilin33/airtest_manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)