from setuptools import setup

setup(
    name = 'iqoptionapi-simple',
    version = '0.0.1',
    author = 'Julian de Almeida Santos',
    author_email = 'julian.santos.info@gmail.com',
    packages = ['iqoptionapi-simple'],
    description = 'API for iq option implemented on the Lu-Yi-Hsun version.',
    long_description = 
    """
        API for iq option implemented on the Lu-Yi-Hsun version.
        This api is wrapper to on [iqoptionapi](https://github.com/iqoptionapi/iqoptionapi).
    """,
    url = 'https://github.com/juliansantosinfo/iqoptionapi-simple',
    project_urls = {
        'Código fonte': 'https://github.com/juliansantosinfo/iqoptionapi-simple',
        'Download': 'https://github.com/juliansantosinfo/iqoptionapi-simple/archive/0.0.1.zip'
    },
    license = 'GPL3',
    keywords = ['iqoptionapi', ''],
    install_requires = [
        "websocket-client==0.56"
    ],
    dependency_links=[
        'git+git://github.com/iqoptionapi/iqoptionapi.git',
    ],
)
