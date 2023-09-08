# `halpy`: an example Python project

> A python library to interact with [HAL API](https://api.archives-ouvertes.fr/docs/search)

## Installation

This project is delivered as a Python package. It can be installed using `pip`:

```bash
python -m pip install git+https://github.com/py4shs/halpy
```

## Usage

A simple Python class is available at the moment: `HALCLient`. It can be used to make requests against `HAL` API:

```python
from pathlib import Path
from halpy import HALClient


client = HALClient()


response = client.search(
    query="python",
    include_fields=["docid", "label_s", "abstract_s"],
    before=2019,
    after=2012,
    rows=100,
    offset=0,
)

Path("result.json").write_text(response.text)
```

The code above search for:

- documents with the keyword `python`
- published before 2019 (excluded)
- published after 2012 (included)

It returns 100 results, from the first result available.

The response will indicate total number of documents available (857 in this case). It's up to users to execute queries
within a for loop and incrementing the offset for each query (i.e., users must handle pagination by themselves).

## Possible exercices

1. Modify the `HALClient.search()` method so that it automatically handles pagination for the users, and sends several requests until all available results are fetched.
