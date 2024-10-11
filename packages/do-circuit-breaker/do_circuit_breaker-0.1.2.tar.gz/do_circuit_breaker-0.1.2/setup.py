# setup.py

from setuptools import setup, find_packages

setup(
    name='do_circuit_breaker',
    version='0.1.2',
    description='A custom circuit breaker for Airflow jobs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ankur Kumar',
    author_email='ankur.kumar@rakuten.com',
    url='https://github.com/ankurrakuten/do_circuit_breaker',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
