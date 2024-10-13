#!/usr/bin/env python3

import re
import sys
import os
from setuptools import setup


SRC = os.path.abspath(os.path.dirname(__file__))


def get_version():
    with open(os.path.join(SRC, 'nexuss/__init__.py')) as f:
        for line in f:
            m = re.match("__version__ = '(.*)'", line)
            if m:
                return m.group(1)
    raise SystemExit("Could not find version string.")


if sys.version_info < (3, 8):
    sys.exit('nexuss requires Python >= 3.8.')

requirements = ['requests>=2.4']
optional_requirements = {
    'browser_cookie3': ['browser_cookie3>=0.19.1'],
}

keywords = (['instagram', 'instagram-scraper', 'instagram-client', 'instagram-feed', 'downloader', 'videos', 'photos',
             'pictures', 'instagram-user-photos', 'instagram-photos', 'instagram-metadata', 'instagram-downloader',
             'instagram-stories'])

# NOTE that many of the values defined in this file are duplicated on other places, such as the
# documentation.

setup(
    name='nexuss',
    version=get_version(),
    packages=['nexuss'],
    package_data={'nexuss': ['py.typed']},
    url='https://nexuss.github.io/',
    license='MIT',
    author='Alexander Graf, André Koch-Kramer',
    author_email='mail@agraf.me, koch-kramer@web.de',
    description='Download pictures (or videos) along with their captions and other metadata '
                'from Instagram.',
    long_description=open(os.path.join(SRC, 'README.rst')).read(),
    install_requires=requirements,
    python_requires='>=3.8',
    extras_require=optional_requirements,
    entry_points={'console_scripts': ['nexuss=nexuss.__main__:main']},
    zip_safe=False,
    keywords=keywords,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Multimedia :: Graphics'
    ]
)
