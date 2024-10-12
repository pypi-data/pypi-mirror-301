from setuptools import setup, find_packages

setup(
    name="hayatapps_paservice_api",
    version="0.1",
    author="Roman Połchowski",
    author_email="rp@hayatapps.com",
    description="PA proto package",
    packages=find_packages(),
    install_requires=[
        'protobuf==5.26.1',
        'grpcio==1.66.2',
        'grpcio-tools==1.66.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)