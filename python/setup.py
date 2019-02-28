from setuptools import setup, find_packages

setup(
    name="openfaas-client",
    install_requires=['requests', 'simplejson', 'urllib3', 'kubernetes'],
    version="0.1.0",
    packages=find_packages(),
    author="Garrett Bates",
    author_email="gbates101@gmail.com",
    description="Wrapper for making API calls to OpenFaaS gateway.",
    license="MIT",
    keywords="openfaas faas api gateway",
    #url="http://example.com/HelloWorld/",   # project home page, if any
    project_urls={
        "Source Code": "https://github.com/gbates101/openfaas-client/tree/master/python",
    }
)
