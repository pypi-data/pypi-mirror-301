from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()
setup(
    name='nepal_const_doc_chunker',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'loguru==0.7.2',
        'langchain-community==0.2.17',
        'pypdf==5.0.0'
    ],
    long_description=description,
    long_description_content_type='text/markdown',
)