from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="my-funded-grpc-api",
    version="0.1.2",
    author="Simeon Aleksov",
    author_email="aleksov_s@outlook.com",
    description="Proto definitions for MyFunded gRPC API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MyFunded/my-funded-grpc-api-proto",
    packages=find_packages(include=['my_funded_grpc_api_proto', 'my_funded_grpc_api_proto.*']),
    package_data={
        'my_funded_grpc_api_proto': ['**/*.py', '**/*.pyi', '**/*.proto'],
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
