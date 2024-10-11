import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='zhutools',
    version='0.0.2',
    packages=setuptools.find_packages(),
    url='https://github.com/GodsLeft/',
    license='MIT',
    author='yaguangzhu@qq.com',
    description='我的个人python工具库',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)