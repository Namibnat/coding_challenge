"""Test content retrieval routine"""

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
        # Sample config data (if any)
    }


def test_data_extractor_initialization(sample_html, sample_config):
    de = DataExtractor(sample_html, sample_config)
    assert de.html == sample_html
    assert de.config == sample_config
    assert de.top_node_descendants is None
    assert de.output_data == {}


def test_get_top_node_descendants(sample_html, sample_config):
    de = DataExtractor(sample_html, sample_config)
    de.get_top_node_descendants()
    assert de.top_node_descendants is not None
    # Assuming there are 4 products in the sample HTML
    assert len(de.top_node_descendants) == 4
