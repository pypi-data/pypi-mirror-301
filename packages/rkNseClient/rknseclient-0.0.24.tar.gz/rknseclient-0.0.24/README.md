# rkNseClient

A brief description of what this project does and who it's for.

## Installation

You can install the package using pip:

```bash
pip install rkNseClient
```

## Usage

Here's a quick example of how to use the package:

```python
from rkNseClient import NSEClient

nse_client = NSEClient()
allStock = nse_client.getEquityList()

for eachStock in allStock:
    print(eachStock.symbol, eachStock.nameOfCompany)
```


## Contributing

Contributions are always welcome!
