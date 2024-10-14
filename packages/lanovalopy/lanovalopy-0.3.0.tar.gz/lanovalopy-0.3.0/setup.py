# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lano_valo_py', 'lano_valo_py.valo_types']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.10.10,<4.0.0', 'asyncio>=3.4.3,<4.0.0', 'pydantic>=2.9.2,<3.0.0']

setup_kwargs = {
    'name': 'lanovalopy',
    'version': '0.3.0',
    'description': 'This is a wrapper for the Valorant API, source: https://github.com/henrikdev/valorant-api',
    'long_description': '[discord]: https://discord.gg/wF9JHH55Kp\n\n<div align="center">\n\n[![Downloads](https://static.pepy.tech/badge/lanovalopy)](https://pepy.tech/project/lanovalopy)\n\n</div>\n\n# LanoValoPy (Lanore Valorant Python)\n\nLanoValoPy is a python-based wrapper for the following Valorant Rest API:\n\nhttps://github.com/Henrik-3/unofficial-valorant-api\n\nThis API is free and freely accessible for everyone. An API key is optional but not mandatory. This project is NOT being worked on regularly.\n\nThis is the first version. There could be some bugs, unexpected exceptions or similar. Please report bugs on our [discord].\n\n### API key\n\nYou can request an API key on [Henrik\'s discord server](https://discord.com/invite/X3GaVkX2YN) <br> It is NOT required to use an API key though!\n\n## Summary\n\n1. [Introduction](#introduction)\n2. [Download](#download)\n3. [Documentation](#documentation)\n4. [Support](#support)\n\n## Introduction\n\nSome requests may take longer.\n\n### Get Account and mmr informations\n\n```python\nimport asyncio\nfrom lano_valo_py import LanoValoPy\nfrom lano_valo_py.valo_types.valo_enums import MMRVersions, Regions\n\nasync def main():\n    # Initialize the API client with your token\n    api_client = LanoValoPy(token="YOUR_TOKEN_HERE")\n\n    # Example: Get Account Information\n    account_options = AccountFetchOptionsModel(name="LANORE", tag="evil")\n    account_response = await api_client.get_account(account_options)\n    print(account_response)\n\n    # Example: Get MMR by PUUID\n    mmr_options = GetMMRFetchOptionsModel(\n        version=MMRVersions.v1,\n        region=Regions.eu,\n        name="Lanore",\n        tag="evil",\n    )\n    mmr_response = await api_client.get_mmr(mmr_options)\n    print(mmr_response)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n\n```\n\n## Download\n\n``` bash\npip install lanovalopy\n\n```\n\n## Documentation\n\nThe detailed documentations are still in progress.\n\n## Support\n\nFor support visit my [discord] server',
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
