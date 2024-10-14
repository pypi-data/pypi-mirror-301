from setuptools import find_packages, setup

setup(
    name="ntanh",  # tên của gói thư viện
    version="0.1.2",
    description="Thư viện hữu ích của Tuấn Anh.",
    url="https://github.com/ntanhfai/tact",
    author="Tuấn Anh - Foxconn",
    author_email="nt.anh.fai@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "ruamel.yaml",
    ],
    readme="README.rst",
    Homepage="https://github.com/ntanhfai/tact",
    Issues="https://github.com/ntanhfai/tact/issues",
)
