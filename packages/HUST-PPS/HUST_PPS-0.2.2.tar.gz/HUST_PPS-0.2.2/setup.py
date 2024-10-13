from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='HUST_PPS',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[
        'numpy>=2.1.1',
    ],
    long_description=Path("README.md").read_text(encoding='utf-8'),  # Đặt mã hóa UTF-8
    long_description_content_type="text/markdown",
)