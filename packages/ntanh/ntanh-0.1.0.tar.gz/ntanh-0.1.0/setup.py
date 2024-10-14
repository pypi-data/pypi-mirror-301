from setuptools import find_packages, setup

setup(
    name="ntanh",
    version="0.1.0",
    description="An python parametters library.",
    url="https://github.com/ntanhfai/tact",
    author="Tuấn Anh - Foxconn",
    author_email="nt.anh.fai@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "ruamel.yaml",
    ],
)
