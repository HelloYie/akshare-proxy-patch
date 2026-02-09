from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="akshare-proxy-patch",  # 包名，用户 pip install 时的名称
    version="0.2.4",  # 版本号
    author="cheapproxy.net",
    author_email="emezxyj1@gmail.com",
    description="AkShare 报错全局Hook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/helloyie/akshare-proxy-patch",  # 项目主页
    packages=find_packages(),  # 自动查找项目中的包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # 对 Python 版本的要求
    install_requires=[  # 核心依赖：安装此包时会自动安装这些
        "requests",
    ],
    include_package_data=True,
)
