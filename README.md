# EIA_API_v2_Python
`eiapy_v2` is a Python module designed to simplify interaction with the U.S. Energy Information Administration (EIA) API v2. 
This module allows you to fetch data for specific series, multiple series, and search by keywords using flexible query parameters.

## Features
- Fetch data for single or multiple series.
- Perform flexible queries with custom parameters.
- Export data to CSV for easy analysis.
## Installation
Make sure you have `requests` and `pandas` installed:
```bash
pip install requests pandas

## Usage
```python
from eiapy_v2 import EIAQuery, export_to_csv

API_KEY = 'YOUR_API_KEY'

# Initialize the EIAQuery class
eia_query = EIAQuery(API_KEY)

# Define the query
base_url = 'https://api.eia.gov/v2/electricity/retail-sales/data/'
params = {
    'frequency': 'annual',
    'data[0]': 'sales',
    'facets[stateid][]': 'IN',
    'start': '2020',
    'end': '2021',
    'sort[0][column]': 'period',
    'sort[0][direction]': 'desc'
}

# Fetch data and export to CSV
data = eia_query.get_data(base_url, params)
export_to_csv(data, 'electricity_retail_sales.csv')

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
This project is partly based on [systemcatch/eiapy](https://github.com/systemcatch/eiapy). 
I made modifications to support EIA API v2 and added additional features like flexible query parameters and CSV export.

