from setuptools import find_packages, setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ntanh",  # tên của gói thư viện
    version="0.1.6.2",
    description="Thư viện hữu ích của Tuấn Anh.",
    url="https://github.com/ntanhfai/tact",
    author="Tuấn Anh - Foxconn",
    author_email="nt.anh.fai@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "ruamel.yaml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "ntanh"},
    # packages=find_packages(where="ntanh"),
    Homepage="https://github.com/ntanhfai/tact",
    Issues="https://github.com/ntanhfai/tact/issues",
)
