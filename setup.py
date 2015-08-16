from setuptools import setup


def get_version(fname='flake8_quotes.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


setup(
    name='flake8-quotes2',
    description='flake8 plugin for string quotes checking',
    license='MIT',
    long_description=open('README.rst').read(),
    author='Javier Domingo Cansino',
    author_email='javierdo1@gmail.com',
    version=get_version(),
    url='https://github.com/txomon/flake8-quotes',
    py_modules=['flake8_quotes'],
    install_requires=['setuptools'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
    entry_points={
        'flake8.extension': ['Q1 = flake8_quotes:QuotesChecker'],
    },
)
