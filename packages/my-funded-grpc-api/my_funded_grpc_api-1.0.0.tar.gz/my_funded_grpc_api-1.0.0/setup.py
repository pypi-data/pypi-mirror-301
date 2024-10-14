from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
root_directory = this_directory
long_description = (root_directory / "README.md").read_text()

setup(
    name="my-funded-grpc-api",
    version='1.0.0',
    author="Simeon Aleksov",
    author_email="aleksov_s@outlook.com",
    description="gRPC API for My Funded trading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MyFunded/my-funded-grpc-api",
    packages=find_packages(),
    package_data={
        'my_funded_grpc_api': ['**/*.py', '**/*.pyi'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "grpcio>=1.32.0",
        "protobuf>=3.14.0",
    ],
)
