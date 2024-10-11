from setuptools import setup, find_packages

setup(
    name='qr_code_lib',
    version='1.0.0',    
    description="Python project to encode/decode QR Code",
    author="Abhilash Sanne",
    author_email="sanne.abhi@gmail.com",
    url="https://github.com/abhilashsanne/qr_code_lib",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
