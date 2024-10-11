# setup.py

from setuptools import setup, find_packages

setup(
    name='sql_scan',
    version='0.2',
    description='SQL file processing package for extracting table names and WHERE conditions',
    author='Meghsham Jambhulkar',
    author_email='meghshamofficial@gmail.com',
    packages=find_packages(),
    install_requires=['sqlparse'],
    entry_points={
        'console_scripts': [
            'sql_scan=sql_scan:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
