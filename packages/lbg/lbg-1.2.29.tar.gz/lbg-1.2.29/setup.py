#!/usr/bin/env python
import setuptools

from lbgcli.meta import version

setuptools.setup(name='lbg',
                 version=version,
                 description='Lebesgue Utility',
                 author='DP Technology',
                 packages=setuptools.find_packages(),
                 author_email='zhangzw@dp.tech',
                 url='https://bohrium.dp.tech/',
                 python_requires='>=3.7',
                 install_requires=['oss2', 'requests', 'requests-toolbelt', 'aliyun-python-sdk-core',
                                   'aliyun-python-sdk-kms', 'aliyun-python-sdk-sts', 'tqdm', 'pytimeparse', 'pyyaml',
                                   'pandas', 'colorama', 'readchar', 'pyreadline', 'pyreadline3', 'validators',
                                   'packaging', 'pyhumps', 'argcomplete'],
                 entry_points={
                     'console_scripts': [
                         'lbg=lbgcli.main_entry:main'
                     ]
                 }
                 )
