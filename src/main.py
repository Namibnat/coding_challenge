"""Fetch, Extract and Save Routine"""

import os
import json
from dotenv import load_dotenv

from scraper import Scraper
from data_extractor import DataExtractor


def _get_config():
    """Load the required config file"""
    load_dotenv()
    config_file = os.getenv('CONFIG_FILE')
    with open(f'config/{config_file}') as fp:
        return json.load(fp)


def main():
    """Main Runner

    Collects product details from a website and saves the data for products within a specified category
    """
    config = _get_config()

    # Fetch html
    scraper = Scraper(config['scraper'])
    html = scraper.get_data()

    # Extract data
    extractor = DataExtractor(html, config['extractor'])
    extractor.get_top_node_descendants()
    extractor.find_items_by_config()

    # Save Data
    extractor.export_data_as_json()


if __name__ == '__main__':
    main()
