from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess


class CustomBuild(build_py):
    """
    The CustomBuild class overrides the run method to compile the .proto files before proceeding w/ the standard
    build process.

    This ensures that the latest generated files are always included when building the package.
    """
    def run(self):
        # Compile the .proto files
        subprocess.check_call([
            'python', '-m', 'grpc_tools.protoc',
            '-I.', '--python_out=quant_proto', '--grpc_python_out=quant_proto',
            'quant_proto/quant.proto'
        ])
        super().run()


setup(
    name='quant-proto',
    version='0.1.0',
    description='Protobuf definitions for Quant services',
    author="AnthroSpark",
    author_email="admin@anthrospark.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'protobuf==4.24.3',
        'grpcio==1.58.0',
    ],
    cmdclass={
        'build_py': CustomBuild,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
