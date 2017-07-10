from setuptools import setup

setup(
    name='lwe-mapper',
    version='1.1.0',
    description='A simple URL-Scheme resolver',
    long_description='For an overview and some examples, head over to'
                     '`Github <https://github.com/linuxwhatelse/mapper>`_',
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
