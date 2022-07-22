from setuptools import setup, find_packages

VERSION = '0.1'

install_requires = []

setup(
    # 必要信息
    name='LANCommunicate',  # 模块名称
    version=VERSION,
    author="Ethan_TheMilkyWay",  # Pypi用户名称
    author_email='1967527237@qq.com',  # Pypi用户的邮箱
    description='project made by ZJX -- CHINA, CAU, CIEE, major in CS, grade 2017',
    url='https://github.com',  # 项目主页
    packages=find_packages(),  # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包

    # 其他信息
    classifiers=[  # 参数说明包的分类信息
        # 分类信息详见https://pypi.org/pypi?%3Aaction=list_classifiers
        'Topic :: Software Development',  # 属于什么类型
        'Intended Audience :: Developers',  # 开发的目标用户
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='python LAN auto data transmission',  #


    install_requires=install_requires,  # 表明当前模块依赖哪些包，若环境中没有，则会从pypi中下载安装
    setup_requires=[],                  # 这里列出的包，不会自动安装。
    # tests_require=["numpy>=1.8"],       # 仅在测试时需要使用的依赖，在正常发布的代码中是没有用的。
    # 在执行python setup.py test时，可以自动安装这三个库，确保测试的正常运行。
    # test_suite='runtests.runtests',

    dependency_links=[                               # 用于安装setup_requires或tests_require里的软件包
        # "http://example2.com/p/foobar-1.0.tar.gz", # 这些信息会写入egg的 metadata 信息中
    ],
    # install_requires 在安装模块时会自动安装依赖包
    # 而 extras_require 不会，这里仅表示该模块会依赖这些包
    # 但是这些包通常不会使用到，只有当你深度使用模块时，才会用到，这里需要你手动安装
    extras_require={
        # 'PDF': ["ReportLab>=1.2", "RXP"],
        # 'reST': ["docutils>=0.3"],
    },
    # python_requires='>=2.7, <=3',  # 关于安装环境的限制

    # 用来支持自动生成脚本，安装后会自动生成 /usr/bin/foo 的可执行文件
    # 该文件入口指向 foo/main.py 的main 函数
    entry_points={
        # 'console_scripts': ['foo = foo.main:main']
    },
    # license='MIT',  # 开源许可证类型

    # 将 bin/foo.sh 和 bar.py 脚本，生成到系统 PATH中
    # 执行 python setup.py install 后
    # 会生成 如 /usr/bin/foo.sh 和 如 /usr/bin/bar.py
    # scripts=['bin/foo.sh', 'bar.py']
)

"""

 # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片等
    data_files=[
        ('', ['conf/*.conf']),
        ('/usr/lib/systemd/system/', ['bin/*.service']),
    ],

    # 希望被打包的文件
    package_data={
        '': ['*.txt'],   # 所有根目录下的以 txt 为后缀名的文件，都会分发
        'bandwidth_reporter': ['*.txt']
    },
    # 不打包某些文件
    exclude_package_data={
        'bandwidth_reporter': ['*.txt']
    },
"""
