# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2024 Jiayu Geng
# Based on original work by Chris Brown (systemcatch/eiapy)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import requests
import pandas as pd

class EIAError(Exception):
    """Custom exception for handling EIA API related errors."""
    pass

class Series:
    """
    Fetches data from the EIA API v2 for a specific series ID.
    """
    def __init__(self, series_id, api_key):
        self.series_id = series_id
        self.api_key = api_key

    def get_data(self):
        """Fetches data using the provided series ID."""
        url = f'https://api.eia.gov/v2/seriesid/{self.series_id}?api_key={self.api_key}'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if 'error' in data:
                raise EIAError(data['error']['message'])
            return data
        except requests.exceptions.RequestException as e:
            raise EIAError(f"Request failed: {e}")
        except ValueError as e:
            raise EIAError(f"JSON parsing failed: {e}")

class MultiSeries:
    """
    Fetches data from the EIA API v2 for multiple series IDs.
    """
    def __init__(self, series_ids, api_key):
        self.series_ids = series_ids
        self.api_key = api_key

    def get_data(self):
        """Fetches data using multiple series IDs."""
        series_str = ','.join(self.series_ids)
        url = f'https://api.eia.gov/v2/seriesid/{series_str}?api_key={self.api_key}'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if 'error' in data:
                raise EIAError(data['error']['message'])
            return data
        except requests.exceptions.RequestException as e:
            raise EIAError(f"Request failed: {e}")
        except ValueError as e:
            raise EIAError(f"JSON parsing failed: {e}")

class Search:
    """
    Searches for EIA data series based on a search value.
    """
    def __init__(self, search_value, api_key):
        self.search_value = search_value
        self.api_key = api_key

    def search_by_name(self):
        """Searches the EIA database using a keyword."""
        url = f'https://api.eia.gov/v2/search/?search_value={self.search_value}&api_key={self.api_key}'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if 'error' in data:
                raise EIAError(data['error']['message'])
            return data
        except requests.exceptions.RequestException as e:
            raise EIAError(f"Request failed: {e}")
        except ValueError as e:
            raise EIAError(f"JSON parsing failed: {e}")

class EIAQuery:
    """
    Class to interact with EIA API v2 using flexible parameters.
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def get_data(self, base_url, params=None):
        """
        Fetch data from the EIA API using a flexible URL and parameters.

        :param base_url: The base URL for the EIA API endpoint.
        :param params: A dictionary of query parameters to include in the request.
        :return: The JSON response as a dictionary.
        """
        if params is None:
            params = {}
        
        # Add the API Key to the request parameters
        params['api_key'] = self.api_key
        
        # Send a GET request to the EIA API
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                raise EIAError(data['error']['message'])
            
            return data
        except requests.exceptions.RequestException as e:
            raise EIAError(f"Request failed: {e}")
        except ValueError as e:
            raise EIAError(f"JSON parsing failed: {e}")

def export_to_csv(data, filename):
    """Export EIA API data to a CSV file."""
    if 'response' in data and 'data' in data['response']:
        df = pd.DataFrame(data['response']['data'])
        df.to_csv(filename, index=False)
        print(f"Data successfully exported to {filename}")
    else:
        print("No data available to export.")
