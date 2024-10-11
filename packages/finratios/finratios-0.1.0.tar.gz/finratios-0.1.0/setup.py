# setup.py

from setuptools import setup, find_packages

setup(
    name='finratios',
    version='0.1.0',
    description='A package to calculate financial ratios of NIF A3 from stock companies and export them to Excel',
    author='Josué Daniel Cepeda Obregón',
    author_email='jcepedaobregon@gmail.com',
    url='https://github.com/josuecepeda94/finratios',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'yfinance',
        'XlsxWriter',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)


