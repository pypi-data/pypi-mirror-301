from setuptools import setup, find_packages

setup(
    name="trace_generator",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    description="A package for generating random traces based on sequence schemas",
    author="Dr. Kovacs Laszlo",
    author_email="laszlo.kovacs@uni-miskolc.hu",
    url="https://github.com/alijlidi/trace_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
