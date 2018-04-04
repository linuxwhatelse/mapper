import os
from setuptools import setup


here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='lwe-mapper',
    version='1.2.5',
    description='A simple URL-Scheme resolver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/linuxwhatelse/mapper',
    author='linuxwhatelse',
    author_email='info@linuxwhatelse.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='url scheme resolver mapper',
    py_modules=[
        'mapper'
    ],
)
