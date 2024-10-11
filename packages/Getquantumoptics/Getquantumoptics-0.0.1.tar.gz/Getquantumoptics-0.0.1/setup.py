from setuptools import setup, find_packages

setup(
    name="Getquantumoptics",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["numpy==2.0.2"],  # 在此列出依赖
    author="GetlinDu",
    author_email="1578440935@qq.com",
    description="A brief quantum simulator of the quantum optics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GetlinDu/Getquantumoptics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)
