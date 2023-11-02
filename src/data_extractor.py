"""This module extracts the required product details and converts it to JSON"""

from bs4 import BeautifulSoup
import json


class DataExtractor:
    """Extract Data and provide output"""
    def __init__(self, html, config):
        self.html = html
        self.config = config
        self.top_node_descendants = None
        self.output_data = {}

    def get_top_node_descendants(self):
        """Extract the top node from the data"""
        soup = BeautifulSoup(self.html, 'html.parser')
        div_contents = soup.find('div', class_='content')
        self.top_node_descendants = div_contents.find_all('div', class_='products')

    def find_items_by_config(self):
        """Find the items as required by the config json"""
        pass

    def export_data_as_json(self):
        try:
            with open('output/filename.json', 'w') as fp:
                json.dump(self.output_data, fp)
        except IOError as e:
            print(f"Data could not be written to file: {e}")
