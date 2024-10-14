from setuptools import setup, find_packages

setup(
    name='tool_scripts',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[],  # 依赖包列表
    author='pww',
    author_email='2118969873pww@gmail.com',
    description='自制各种脚本',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/您的用户名/mypackage',  # 项目的URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # Python版本要求
)
