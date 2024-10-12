# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lano_valo_py']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.10.10,<4.0.0', 'asyncio>=3.4.3,<4.0.0', 'pydantic>=2.9.2,<3.0.0']

setup_kwargs = {
    'name': 'lanovalopy',
    'version': '0.1.0',
    'description': 'This is a wrapper for the Valorant API, source: https://github.com/henrikdev/valorant-api',
    'long_description': '# LanoValoPy',
    'author': 'Lanxre',
    'author_email': '73068449+Lanxre@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
