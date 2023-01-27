"""
File needed to create package
"""

from setuptools import setup

setup(
    name='source',
    version='0.1.0',
    description='A Python package to explore FRED API',
    url='https://github.com/Diana0422/frappy.git',
    author='Mattia Antonangeli, Diana Pasquali',
    author_email='mattiaantonangeli@gmail.com, diamerita@gmail.com',
    license='',
    packages=['source'],
    install_requires=['pandas',
                      'numpy',
                      'plotly',
                      'requests',
                      'python-kaleido'
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
