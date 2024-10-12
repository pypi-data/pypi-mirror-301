from setuptools import setup, find_packages

setup(
    name="netcup-webservice",
    version="0.1.4",
    description="Unofficial Python client for Netcup Webservice API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/mihneamanolache/netcup-webservice",
    author="Mihnea-Octavian Manolache",
    author_email="me@mihnea.dev",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "zeep",  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

