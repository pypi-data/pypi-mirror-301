[discord]: https://discord.gg/wF9JHH55Kp


# LanoValoPy (Lanore Valorant Python)

LanoValoPy is a python-based wrapper for the following Valorant Rest API:

https://github.com/Henrik-3/unofficial-valorant-api

This API is free and freely accessible for everyone. An API key is optional but not mandatory. This project is NOT being worked on regularly.

This is the first version. There could be some bugs, unexpected exceptions or similar. Please report bugs on our [discord].

### API key

You can request an API key on [Henrik's discord server](https://discord.com/invite/X3GaVkX2YN) <br> It is NOT required to use an API key though!

## Summary

1. [Introduction](#introduction)
2. [Download](#download)
3. [Documentation](#documentation)
4. [Support](#support)

## Introduction

Some requests may take longer.

### Get Account and mmr informations

```python
import asyncio
from lano_valo_py import LanoValoPy

async def main():
    api = LanoValoPy(token="YOUR_TOKEN_HERE")

    # Get account details
    account_data = await api.get_account(name="LANORE", tag="evil")
    if account_data.error:
        print(f"Error {account_data.status}: {account_data.error}")
    else:
        print(f"Account Data: {account_data.data}")

    # Get MMR
    mmr_data = await api.get_mmr(version="v1", region="eu", name="LANORE", tag="evil")
    if mmr_data.error:
        print(f"Error {mmr_data.status}: {mmr_data.error}")
    else:
        print(f"MMR Data: {mmr_data.data}")


if __name__ == "__main__":
    asyncio.run(main())

```

## Download

``` bash
pip install lanovalopy

```

## Documentation

The detailed documentations are still in progress.

## Support

For support visit my [discord] server