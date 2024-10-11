from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='lib_service_transport',
    version='0.0.13',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'lib_service_transport'},
    packages=find_packages(where='lib_service_transport'),
    url='https://gitlab.it-rs.ru/askona/lib-service-transport',
    author='',
    author_email='intelligent174@mail.ru',
    license='Apache Software License',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    install_requires=['pika', 'pika-stubs', 'pydantic-settings', 'orjson'],
    extras_require={
        'dev': ['twine>=5.1.1'],
    },
    python_requires='>=3.12',
)
