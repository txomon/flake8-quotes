from setuptools import setup

def get_version(fname='flake8_quotes.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

setup(
    name='flake8-quotes',
    description='flake8 plugin for string quotes checking',
    license='MIT',
    long_description=open('README.rst').read(),
    author='Javier Domingo Cansino',
    author_email='javierdo1@gmail.com',
    version=get_version(),
    url='https://github.com/txomon/flake8-quotes',
    py_modules=['flake8_quotes'],
    install_requires=[
        'setuptools',
        'flake',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'flake8.extension': ['flake8_quotes = flake8_quotes:QuotesChecker'],
    },
)
