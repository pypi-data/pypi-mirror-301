from setuptools import setup, find_packages

setup(
    name='MirrorMate',
    version='0.1',
    description='A tool to clone websites and download specific files using wget',
    author='MrFidal',
    author_email='mrfidal@proton.me',
    url='https://github.com/ByteBreach/MirrorMate',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mirrormate=mirrormate.cli:main',
        ],
    },
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
