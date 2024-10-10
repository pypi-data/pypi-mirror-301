from setuptools import setup, find_packages

setup(
    name='myPackageA',       # 包名
    version='0.1',
    packages=find_packages(include=['demo']),  # 仅包含 demo 文件夹
    package_data={           # 指定要包含的数据文件
        '': ['*.py', '*.txt'],   # 包含所有 .py 和 .txt 文件
        'demo': ['*.txt'],        # 如果 demo 中有特定的 txt 文件，添加这个条目
    },
    install_requires=[              # 从 requirements.txt 中读取依赖
        line.strip() for line in open('requirements.txt').readlines() if line.strip()
    ],
    author='Catherine',             # 作者名字
    author_email='3350249641@qq.com',  # 作者邮箱
    description='just a test',  # 描述
    long_description=open('README.md').read(),  # 可选
    long_description_content_type='text/markdown',  # 可选
    url='https://github.com/1Catherine137/myPackageA',  # 项目的 URL
    license='MIT',                  # 许可证类型
    classifiers=[                   # 分类
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)