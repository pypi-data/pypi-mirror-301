from setuptools import setup, find_packages

setup(
    name="qz_cal",  # 包的名称
    version="1.0.0",  # 初始版本号
    author="Your Name",
    author_email="your_email@example.com",
    description="A short description of your package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your_package",  # 项目的 GitHub 地址
    packages=find_packages(),  # 自动找到所有的包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 指定许可证
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 指定 Python 版本要求
    install_requires=[  # 列出依赖项  
    ]
)
