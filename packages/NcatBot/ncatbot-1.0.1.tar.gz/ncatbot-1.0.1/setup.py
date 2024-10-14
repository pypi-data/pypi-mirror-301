import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="NcatBot",  # 模块名称
    version="1.0.1",  # 当前版本
    author="buchilizi",  # 作者
    author_email="2793415370@qq.com",  # 作者邮箱
    description="基于Napcat开发的QQ机器人",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="https://github.com/wupeiqi/fucker",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'websocket-client',  # 用于WebSocket连接
        'requests',          # 用于HTTP请求
        'colorama',          # 用于美化日志输出
        'setuptools'         # 用于打包和分发
    ],
    python_requires='>=3',
)