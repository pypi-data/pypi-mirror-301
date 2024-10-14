from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xssniffer',
    version='0.1.0',
    author='Fidal',
    author_email='mrfidal@proton.me',
    description='A package to find XSS vulnerabilities.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/xssniffer',
    packages=find_packages(),
    package_data={
        'xssniffer': ['payload.txt'], 
    },
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'xssniffer=xssniffer.scanner:start_scan',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
