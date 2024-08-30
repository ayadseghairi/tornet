from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tornet',
    version='2.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'requests[socks]',
    ],
    entry_points={
        'console_scripts': [
            'tornet=tornet.tornet:main',
        ],
    },
    author='Ayad Seghiri',
    author_email='seghiri.ayad@univ-khenchela.dz',
    description='TorNet - Automate IP address changes using Tor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ayadseghairi/tornet',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
