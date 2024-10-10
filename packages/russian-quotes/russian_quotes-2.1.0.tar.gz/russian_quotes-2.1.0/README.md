[![Downloads](https://static.pepy.tech/badge/russian-quotes)](https://pepy.tech/project/russian-quotes)
[![Downloads](https://static.pepy.tech/badge/russian-quotes/month)](https://pepy.tech/project/russian-quotes)
[![Downloads](https://static.pepy.tech/badge/russian-quotes/week)](https://pepy.tech/project/russian-quotes)

# russian_quotes

## Installation
```shell
pip install russian-quotes
```

## Usage
* **Sync**
```py
from russian_quotes import get_quote, Languages

text, author = get_quote(lang=Languages.ENGLISH)

print(f'Quote: {text} Author: {author}')
```
* **Async**
```py
import asyncio
from russian_quotes import get_quote_async, Languages


async def main():
    return await get_quote_async(lang=Languages.ENGLISH)

text, author = asyncio.run(main())

print(f'Text: {text} Author: {author}')
```
* **Catching of exception**
```py
import russian_quotes

try:
    text, author = russian_quotes.get_quote()
    print(f'Text: {text} Author: {author}')

except russian_quotes.ServerError:
    print('Error!')
```

## Dependencies

[Python >=3.7](https://www.python.org/downloads/release/python-310)

## Legal

[MIT](http://en.wikipedia.org/wiki/MIT_License)
