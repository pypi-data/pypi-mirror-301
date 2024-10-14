from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


packages = find_packages(include=['my_funded_grpc_api', 'my_funded_grpc_api.*', 'trading_account.*', 'trading_account'])
print("Packages found:", packages)

package_data = {}
for package in packages:
    package_path = Path(package.replace('.', '/'))
    package_data[package] = []
    for file_path in package_path.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(package_path)
            package_data[package].append(str(relative_path))

print("Package data:", package_data)

setup(
    name="my-funded-grpc-api-proto",
    version='0.1.3',
    author="Simeon Aleksov",
    author_email="aleksov_s@outlook.com",
    description="Proto definitions for MyFunded gRPC API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MyFunded/my-funded-grpc-api",
    packages=packages,
    package_data=package_data,
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