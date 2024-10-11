from setuptools import setup, find_packages

setup(
    name="trace_generator",
    version="2.0",
    packages=find_packages(),
    install_requires=[],
    description="A package for generating random traces based on sequence schemas..",
    long_description=open('README.md').read(),  # Or wherever your long description is located
    long_description_content_type='text/markdown',  # Specify the format of the long description
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
