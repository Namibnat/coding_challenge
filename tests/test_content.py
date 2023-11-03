"""Test content retrieval routine"""

import os
import pytest

from src.data_extractor import DataExtractor
from src.scraper import Scraper


@pytest.fixture
def sample_html():
    """Load the test HTML for use in multiple tests"""
    with open('tests/assets/html_test.html', 'r') as file:
        return file.read()


@pytest.fixture
def sample_config():
    return {
        'output_filename': 'test_data_file',
        'base_node': {
            'type': 'div',
            'attributes': {
                'class': 'products'
            }
        },
        'child_nodes': {
            'reference': 'product',
            'structure': {
                'node': {
                    'type': 'div',
                    'attributes': 'product',
                    'child_nodes': {
                        'product_name': {
                            'find': {
                                'type': 'h3'
                            },
                            'return': 'text'
                        },
                        'product_image_url': {
                            'find': {
                                'type': 'img'
                            },
                            'return': {
                                'attribute': 'src'
                            }
                        }
                    }
                }
            }
        }
    }


def test_data_extractor_initialization(sample_html, sample_config):
    """Test that the extractor initializes correctly"""
    de = DataExtractor(sample_html, sample_config)
    assert de.html == sample_html
    assert de.config == sample_config
    assert de.top_node is None
    assert de.output_data == {}


def test_data_extractor_config_has_top_node(sample_html, sample_config):
    """Test that the extractor finds the correct items in the config"""
    de = DataExtractor(sample_html, sample_config)
    assert de.config['base_node']['type'] == 'div'
    assert de.config['base_node']['attributes']['class'] == 'products'


def _top_node_helper(sample_html, sample_config):
    """Helper file to set up extractor"""
    de = DataExtractor(sample_html, sample_config)
    de.get_top_node_descendants()
    return de


def test_get_top_node_descendants(sample_html, sample_config):
    """Test that we find the main group top node"""
    de = _top_node_helper(sample_html, sample_config)
    assert de.top_node is not None


def test_find_items_by_config_creates_data_node(sample_html, sample_config):
    """Test that the extractor does create a dictionary of data"""
    de = _top_node_helper(sample_html, sample_config)
    de.find_items_by_config()
    assert isinstance(de.output_data, dict)
    assert 'data' in de.output_data.keys()


def test_find_items_by_config_has_correct_number_fields(sample_html, sample_config):
    """Test that the right number of items are collected from a simple page"""
    de = _top_node_helper(sample_html, sample_config)
    de.find_items_by_config()
    assert len(de.output_data['data']) == 4


def test_find_items_by_config_has_child_categories(sample_html, sample_config):
    """Test that items within the child nodes are returned"""
    de = _top_node_helper(sample_html, sample_config)
    de.find_items_by_config()
    assert 'product' in de.output_data['data'][1].keys()
    assert 'product_name' in de.output_data['data'][1]['product'].keys()
    assert de.output_data['data'][1]['product']['product_name'] == 'Item 2'
    assert de.output_data['data'][3]['product']['product_image_url'] == 'http://test_image_bucket/image4.jpg'


def test_export_data_as_json(sample_html, sample_config):
    """Test to see if the data is exported to the test file"""
    de = _top_node_helper(sample_html, sample_config)
    de.find_items_by_config()
    de.export_data_as_json()
    assert len(os.listdir('output')) > 0


scraper_data = {
    'url': 'https://natureblog.co.uk/'
}


def test_scraper_sets_up_correctly():
    """Test that the scraper initializes as expected"""
    scaper = Scraper(scraper_data)
    assert 'url' in scaper.config.keys()
    assert isinstance(scaper.driver, object)


def test_scraper_gets_html():
    """Use a known website to test if html does get returned from the scraper"""
    scaper = Scraper(scraper_data)
    data = scaper.get_data()
    assert len(data) > 0
    assert '<h1>' in data
