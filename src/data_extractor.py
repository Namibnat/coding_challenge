"""This module extracts the required product details and converts it to JSON"""

from bs4 import BeautifulSoup
import json


class DataExtractor:
    """Extract Data and provide output"""
    def __init__(self, html, config):
        self.html = html
        self.config = config
        self.top_node = None
        self.top_node_descendants = None
        self.output_data = {}

    def get_top_node_descendants(self):
        """Extract the top node from the data"""
        soup = BeautifulSoup(self.html, 'html.parser')
        top_node_config = self.config['base_node']
        self.top_node = soup.find(top_node_config['type'], attrs=top_node_config["attributes"])

    @staticmethod
    def _extract_items(node, children_nodes_config):
        """Extract the items per node required by the config"""
        data = {}
        for item, extraction_data in children_nodes_config.items():
            extraction_item = extraction_data['find']
            return_item = extraction_data['return']
            if 'attributes' in extraction_item.keys():
                try:
                    source_item = node.find(extraction_item['type'], attrs=extraction_item['attributes'])
                except:
                    source_item = "Data not available for this field"
            else:
                try:
                    source_item = node.find(extraction_item['type'])
                except:
                    source_item = "Data not available for this field"
            if isinstance(return_item, str):
                if return_item == 'text':
                    try:
                        data[item] = source_item.text.strip()
                    except:
                        data[item] = "Data not available for this field"

            elif isinstance(return_item, dict):
                try:
                    data[item] = source_item[return_item['attribute']]
                except:
                    data[item] = "Data not available for this field"

        return data

    def find_items_by_config(self):
        """Find the items as required by the config json"""
        self.output_data['data'] = []
        reference = self.config['child_nodes']['reference']
        children_nodes_config = self.config['child_nodes']['structure']
        structure_node = children_nodes_config['node']
        self.top_node_descendants = self.top_node.find_all(structure_node['type'], attrs=structure_node['attributes'])

        for node in self.top_node_descendants:
            item = {reference: self._extract_items(node, structure_node['child_nodes'])}
            self.output_data['data'].append(item)

    def export_data_as_json(self):
        """Save data to data file in output directory"""
        try:
            with open(f"output/{self.config['output_filename']}.json", 'w') as fp:
                json.dump(self.output_data, fp)
        except IOError as e:
            print(f"Data could not be written to file: {e}")
