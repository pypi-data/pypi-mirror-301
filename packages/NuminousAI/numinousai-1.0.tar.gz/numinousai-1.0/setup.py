from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='NuminousAI',
    version='1.0',
    description='A simple package for interacting with URLs and basic functionalities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sujal Rajpoot',
    author_email='sujalrajpoot70@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
