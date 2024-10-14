from setuptools import setup, find_packages

setup(
    name='fget',  # The name of your package on PyPI
    version='0.1.0',  # Version of the package
    description='A powerful file downloader with FTP, HTTP/HTTPS support and advanced features like custom headers, SSL, and proxy.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ethc4',
    author_email='cs7778503@gmail.com',
    url='https://github.com/0625963141-cyber/fget',  # Replace with your repo URL
    license='MIT',  # Choose your preferred license
    packages=find_packages(),  # Automatically finds your package
    install_requires=[
        'requests',  # Required library for HTTP/HTTPS downloads
    ],
    entry_points={
        'console_scripts': [
            'fget=fget.fget:main',  # Exposes fget as a CLI command
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
