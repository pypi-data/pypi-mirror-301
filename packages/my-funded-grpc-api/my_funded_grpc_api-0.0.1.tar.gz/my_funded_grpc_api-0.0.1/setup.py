from pathlib import Path

from setuptools import setup, find_packages
current_dir = Path(__file__).parent
version_file = current_dir.parent / 'version.txt'
print(version_file)
print(current_dir)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="my-funded-grpc-api",
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "protobuf>=3.15.0",
        "grpcio>=1.37.0",
    ],
    author="Simeon Aleksov",
    author_email="aleksov_s@outlook.com",
    description="Python package for MyFunded gRPC API Proto",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MyFunded/my-funded-grpc-api-proto",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)