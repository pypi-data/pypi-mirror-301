from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dsqlenv',
    version='0.0.2',
    author='Zhaosheng',
    author_email='zhaosheng@nuaa.edu.cn',
    description='A tool for database operations with encryption and decryption, configurable table and column names, and additional CLI features.',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'pycryptodome',
        'python-dotenv',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'dsqlenv = dsqlenv.cli:main',
        ]
    }
)
