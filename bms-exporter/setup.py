from os import getenv
from setuptools import find_packages, setup


setup(
    name='bms-exporter',
    version='0.1.0',
    description='Collect bms metrics',
    author='Stefan Andres',
    author_email='stefan@sandres.de',
    license='AGPL',
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3',
    install_requires=[
        'Click',
        'prometheus_client',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bms-exporter=bms_exporter.main:main'
        ]
    }
)

