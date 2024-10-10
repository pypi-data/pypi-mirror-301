#!/usr/bin/env python
import codecs
from admin_honeypot import __version__, __description__, __license__

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

def read_me(filename):
    return codecs.open(filename, encoding='utf-8').read()

setup(
    name='django-admin-honeypot-2024',
    version=__version__,
    description=__description__,
    long_description=read_me('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    keywords='django admin honeypot trap',
    maintainer='xcai',
    maintainer_email='xxiaocai517@gmail.com',
    url='https://github.com/xcai/django-admin-honeypot',
    download_url='https://github.com/xcai/django-admin-honeypot/tarball/v%s' % __version__,
    license=__license__,
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'django-ipware',
    ],
    python_requires='>=3',
)
