from setuptools import setup, find_packages

setup(
    name='mirrormate',
    version='2.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mirrormate = mirrormate.cli:main',
        ],
    },
)
