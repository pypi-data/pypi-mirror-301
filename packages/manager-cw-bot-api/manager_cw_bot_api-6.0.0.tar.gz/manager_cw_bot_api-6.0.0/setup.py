from io import open
from setuptools import setup

"""
:authors: Alexander Laptev, CW
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2024 Alexander Laptev, CW
"""


def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='manager_cw_bot_api',
    version="6.0.0",

    author='Alexander Laptev, CW',
    author_email='cwr@cwr.su',

    description=(
        u'Python LIB for Business users in Telegram '
        u'(For admin - business-person; Manager CW Bot API).\n\n'
        u'📄 </> Documentation: https://docs.cwr.su/\n\n'
        u'If you have any questions, please write to the official email: help@cwr.su.\n\n'
        u'Also, keep an eye on the latest versions of the library.\nThe library uses asynchronous code.'
    ),
    long_description=readme(),
    long_description_content_type='text/markdown',

    url='https://github.com/cwr-su/manager_cw_bot_api',
    download_url='https://github.com/cwr-su/manager_cw_bot_api/archive/refs/heads/main.zip',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['manager_cw_bot_api'],
    install_requires=['PyMySQL', 'aiogram', 'requests', 'yookassa', 'fpdf2'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    project_urls={
        'Documentation': 'https://docs.cwr.su/'
    },
    python_requires='>=3.9'
)
