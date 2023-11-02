"""Test content retrieval routine"""

import os
import pytest
from src.data_extractor import DataExtractor


@pytest.fixture
def sample_html():
    """Load the test HTML for use in multiple tests"""
    with open('tests/assets/html_test.html', 'r') as file:
        return file.read()


@pytest.fixture
def sample_config():
    return {
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
    de = DataExtractor(sample_html, sample_config)
    assert de.html == sample_html
    assert de.config == sample_config
    assert de.top_node is None
    assert de.output_data == {}


def test_data_extractor_config_has_top_node(sample_html, sample_config):
    de = DataExtractor(sample_html, sample_config)
    assert de.config['base_node']['type'] == 'div'
    assert de.config['base_node']['attributes']['class'] == 'products'

def _top_node_helper(sample_html, sample_config):
    de = DataExtractor(sample_html, sample_config)
    de.get_top_node_descendants()
    return de


def test_get_top_node_descendants(sample_html, sample_config):
    de = _top_node_helper(sample_html, sample_config)
    assert de.top_node is not None


def test_find_items_by_config_creates_data_node(sample_html, sample_config):
    de = _top_node_helper(sample_html, sample_config)
    de.find_items_by_config()
    assert de.output_data
    assert 'data' in de.output_data.keys()


def test_find_items_by_config_has_correct_number_fields(sample_html, sample_config):
    de = _top_node_helper(sample_html, sample_config)
    de.find_items_by_config()
    assert len(de.output_data['data']) == 4


def test_find_items_by_config_has_child_categories(sample_html, sample_config):
    de = _top_node_helper(sample_html, sample_config)
    de.find_items_by_config()
    assert 'product' in de.output_data['data'][1].keys()
    assert 'product_name' in de.output_data['data'][1]['product'].keys()
    assert de.output_data['data'][1]['product']['product_name'] == 'Item 2'
    assert de.output_data['data'][3]['product']['product_image_url'] == 'http://test_image_bucket/image4.jpg'


def test_export_data_as_json(sample_html, sample_config):
    de = _top_node_helper(sample_html, sample_config)
    de.find_items_by_config()
    de.export_data_as_json('test_data_file.json')
    assert len(os.listdir('output')) > 0
