# iqoptionapi-simple

**iqoptionapi-simple** ia  API for iq option implemented on the Lu-Yi-Hsun version.
This api is wrapper to on [iqoptionapi](https://github.com/iqoptionapi/iqoptionapi).

## Features

- Class unique with simplified methods.

## Installation

- Run `pip install https://github.com/iqoptionapi/iqoptionapi/archive/refs/tags/7.0.0.tar.gz`
- Run `pip install iqoptionapi-simple`

## Exxemple

```python
from iqoptionapi_simple import IQ_Option

api = IQ_Option(email="julian.santos.trash@gmail.com", password="mypassisiqoption", active_account_type="PRACTICE")

api.connect()

if api.is_connected():
    print(api.get_profile())
```

## Upgrade

- Run `pip install iqoptionapi-simple --upgrade`