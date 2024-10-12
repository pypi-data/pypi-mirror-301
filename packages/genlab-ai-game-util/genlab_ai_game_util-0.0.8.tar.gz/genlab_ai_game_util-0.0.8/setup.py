from setuptools import setup, find_packages

setup(
    name='genlab_ai_game_util',  # 包名
    version='0.0.8',  # 包的版本
    packages=find_packages(),  # 自动寻找包
    install_requires=[  # 列出依赖包
        'redis>=5.1.1',
    ],
    author='hy',  # 作者信息
    author_email='huyang3572@gmail.com',  # 作者邮箱
    description='ai game python',  # 简短描述
    long_description=open('README.md').read(),  # 长描述，通常来自README.md
    long_description_content_type='text/markdown',
    url='',  # 项目主页
    classifiers=[  # 分类器用于包的元数据
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # Python版本要求
)