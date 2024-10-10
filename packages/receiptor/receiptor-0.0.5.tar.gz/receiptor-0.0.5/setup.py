from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'Extract receipt / invoice/ orders data from your gmail .'
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="receiptor",
    version=VERSION,
    author="Omkar Malpure",
    author_email="<malpureomkar5@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
    'aiohttp==3.9.3',
    'pycurl',
    'aiosignal==1.3.1',
    'annotated-types==0.6.0',
    'anyio==4.2.0',
    'attrs==23.2.0',
    'beautifulsoup4==4.12.3',
    'certifi==2024.2.2',
    'cffi==1.16.0',
    'charset-normalizer==3.3.2',
    'cryptography==42.0.2',
    'pycryptodome==3.10.1',
    'Deprecated==1.2.14',
    'fastapi==0.109.2',
    'frozenlist==1.4.1',
    'idna==3.6',
    'jwcrypto==1.5.1',
    'lxml==5.1.0',
    'multidict==6.0.5',
    'pycparser==2.21',
    'pydantic==2.6.1',
    'pydantic_core==2.16.2',
    'PyJWT==2.8.0',
    'PyPDF2==3.0.1',
    'python-docx==1.1.0',
    'python-jwt==4.1.0',
    'requests==2.31.0',
    'sniffio==1.3.0',
    'soupsieve==2.5',
    'typing_extensions==4.9.0',
    'urllib3==2.2.0',
    'wrapt==1.16.0',
    'yarl==1.9.4',
    'google-generativeai==0.3.2',
    'python-dotenv==1.0.1',
    'openai',
    'tiktoken==0.7.0',
    'google_play_scraper',
    'httpx==0.26.0',
    'pyOpenSSL==17.2.0',
    'colorthief'
],
    keywords=['python', 'gmail', 'receipts', 'invoice', 'data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)