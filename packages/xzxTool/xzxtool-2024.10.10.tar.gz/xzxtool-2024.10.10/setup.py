from setuptools import setup
import io
# from setuptools import find_packages

def read(filename):
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return fd.read()

setup(
    name="xzxTool",
    version="2024.10.10",
    author="zhixin",
    author_email="",  # 作者邮箱
    url='',  # github或者自己的网站地址
    description="simple usage",
    long_description_content_type='text/markdown',  # 指定详细描述的文本格式
    long_description=read('README.md'),  #读取文件中介绍包的详细内容
    python_requires=">=3.6.0",  # python依赖版本
    license="MIT Licence",  # 指定许可证
    install_requires=["numpy","pandas"],  # 需要安装的依赖,如["matplotlib", "talib", "pylab", "numpy", "pandas", "baostock"]
    packages=[
        "xzxTool",
    ],  
    platforms="any",
)
