"""
File needed to create package
"""

from setuptools import setup

setup(
    name='frappy',
    version='0.1.0',
    description='A Python package to explore FRED API',
    url='https://github.com/shuds13/pyexample',
    author='Mattia Antonangeli, Diana Pasquali',
    author_email='diamerita@gmail.com, mattiaantonangeli@gmail.com',
    license='',
    packages=['frappy'],
    install_requires=['pandas',
                      'numpy',
                      'plotly',
                      'requests',
                      'sqlite'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
