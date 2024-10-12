from setuptools import setup, find_packages

setup(
    name='mirrormate',
    version='1.0.0',
    packages=find_packages(),
    description='A simple package to clone websites and download specific files using wget.',
    author='MrFidal',
    author_email='mrfidal@proton.me',
    url='https://github.com/ByteBreach/MirrorMate',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
