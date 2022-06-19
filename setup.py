from setuptools import find_packages, setup

setup(
    name='fiicrawler',
    packages=find_packages(),
    version='0.0.2',
    description='Lib to scrap the web for fiis` information',
    author='Marcos Xaxá',
    license='MIT',
    install_requires=[
        'beautifulsoup4==4.10.0',
        "bs4==0.0.1",
        'certifi==2021.10.8',
        'charset-normalizer==2.0.9',
        'dnspython==2.1.0',
        'idna==3.3',
        'pymongo==4.0.1',
        'requests==2.26.0',
        'soupsieve==2.3.1',
        'urllib3==1.26.7',
        'pyparsing',
    ]
)