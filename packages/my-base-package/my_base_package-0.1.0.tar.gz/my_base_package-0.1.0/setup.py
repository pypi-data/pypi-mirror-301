from setuptools import setup, find_packages

setup(
    name="my_base_package",
    version="0.1.0",
    author="Luka",
    author_email="luka.kukhaleishvili.1@iliauni.edu.ge",
    description="A simple package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
 
