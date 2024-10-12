from setuptools import setup, find_packages

setup(
    name='mirrormate',
    version='3.0.0',
    description='A simple package to clone websites and download specific files using wget.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ByteBreach/MirrorMate',
    author='MrFidal',
    author_email='mrfidal@proton.me',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    keywords='mirrormate clone websites wget download files',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mirrormate=mirrormate.cli:main',
        ],
    },
    python_requires='>=3.6',
)
