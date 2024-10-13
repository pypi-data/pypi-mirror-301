from setuptools import setup, find_packages

setup(
    name='dsqlenv',
    version='0.0.1',
    author='Zhaosheng',
    author_email='zhaosheng@nuaa.edu.cn',
    description='A tool for database operations with encryption and decryption, configurable table and column names, and additional CLI features.',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'pycryptodome',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'dsqlenv = dsqlenv.cli:main',
        ]
    }
)
