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
    'version': '0.2.0',
    'description': 'This is a wrapper for the Valorant API, source: https://github.com/henrikdev/valorant-api',
    'long_description': '[discord]: https://discord.gg/wF9JHH55Kp\n\n\n# LanoValoPy (Lanore Valorant Python)\n\nLanoValoPy is a python-based wrapper for the following Valorant Rest API:\n\nhttps://github.com/Henrik-3/unofficial-valorant-api\n\nThis API is free and freely accessible for everyone. An API key is optional but not mandatory. This project is NOT being worked on regularly.\n\nThis is the first version. There could be some bugs, unexpected exceptions or similar. Please report bugs on our [discord].\n\n### API key\n\nYou can request an API key on [Henrik\'s discord server](https://discord.com/invite/X3GaVkX2YN) <br> It is NOT required to use an API key though!\n\n## Summary\n\n1. [Introduction](#introduction)\n2. [Download](#download)\n3. [Documentation](#documentation)\n4. [Support](#support)\n\n## Introduction\n\nSome requests may take longer.\n\n### Get Account and mmr informations\n\n```python\nimport asyncio\nfrom lano_valo_py import LanoValoPy\n\nasync def main():\n    api = LanoValoPy(token="YOUR_TOKEN_HERE")\n\n    # Get account details\n    account_data = await api.get_account(name="LANORE", tag="evil")\n    if account_data.error:\n        print(f"Error {account_data.status}: {account_data.error}")\n    else:\n        print(f"Account Data: {account_data.data}")\n\n    # Get MMR\n    mmr_data = await api.get_mmr(version="v1", region="eu", name="LANORE", tag="evil")\n    if mmr_data.error:\n        print(f"Error {mmr_data.status}: {mmr_data.error}")\n    else:\n        print(f"MMR Data: {mmr_data.data}")\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n\n```\n\n## Download\n\n``` bash\npip install lanovalopy\n\n```\n\n## Documentation\n\nThe detailed documentations are still in progress.\n\n## Support\n\nFor support visit my [discord] server',
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
