# -*- coding:utf-8 -*-
import sys
sys.argv.append('sdist')
from distutils.core import setup
from setuptools import find_packages

setup(name='EsyPro',
            version='39.2024.10.10.11.11',
            packages=['EsyPro',],
            description='a python lib for project files',
            long_description='',
            author='Quanfa',
            include_package_data = True,
            author_email='quanfa@tju.edu.cn',
            url='http://www.xxxxx.com/',
            license='MIT',
            )

            