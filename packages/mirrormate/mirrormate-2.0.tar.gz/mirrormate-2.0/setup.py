from setuptools import setup, find_packages

setup(
    name='mirrormate',
    version='2.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mirrormate = mirrormate.cli:main',
        ],
    },
)
