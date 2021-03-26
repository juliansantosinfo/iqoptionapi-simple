from setuptools import setup

setup(
    name = 'iqoptionapi_simple',
    version = '0.0.1',
    author = 'Julian de Almeida Santos',
    author_email = 'julian.santos.info@gmail.com',
    packages = ['iqoptionapi_simple'],
    description = 'This api is wrapper for iq option implementation of the iqoption version supported by community.',
    long_description = 
    """
        This api is wrapper for implemented on the iqoption supported by community version.
        IQ Option Community [iqoptionapi](https://github.com/iqoptionapi/iqoptionapi).
    """,
    url = 'https://github.com/juliansantosinfo/iqoptionapi_simple',
    project_urls = {
        'Código fonte': 'https://github.com/juliansantosinfo/iqoptionapi_simple',
        'Download': 'https://github.com/juliansantosinfo/iqoptionapi_simple/archive/0.0.1.zip'
    },
    license = 'GPL3',
    keywords = ['iqoptionapi', 'api', 'simple'],
    install_requires = [
        "websocket-client==0.56"
    ],
    dependency_links=[
        'git+git://github.com/iqoptionapi/iqoptionapi.git',
    ],
)