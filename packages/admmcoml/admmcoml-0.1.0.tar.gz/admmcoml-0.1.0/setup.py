from setuptools import setup, find_packages
import sys

setup(
    name="admmcoml",
    version="0.1.0",
    author="Guozheng Wang",  #作者名字
    author_email="gzh.wang@outlook.com",
    description="Convex Optimization Machine Learning Toolkit Based on Distributed ADMM.",
    license="SHU",
    url="https://gzhwanghub.github.io/",  #github地址或其他地址
    packages=find_packages(),
    #package_data={"": ["*"]}, 
    #data_files=[('train_framework', ['train_framework/_train_framework.so'])],
    include_package_data=True,
    install_requires=[
            'mpi4py>=3.1.4'
    ],
    zip_safe=False,
    python_requires='>=3'
)
