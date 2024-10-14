from setuptools import find_packages, setup

setup(
    name="ntanh",  # tên của gói thư viện
    version="0.1.1",
    description="Thư viên hữu ích của Tuấn Anh.",
    url="https://github.com/ntanhfai/tact",
    author="Tuấn Anh - Foxconn",
    author_email="nt.anh.fai@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "ruamel.yaml",
    ],
)
