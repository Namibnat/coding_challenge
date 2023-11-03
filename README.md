# Product Data Scrapper

## Introduction

This Python script is designed to scrape product details.

The output format provides data regarding the products in a JSON format.

## Requirements

Requirements can be found in the requirements.txt file. To run this successfully, set up a python virtual environment and run the following command:

```
pip install -r requirements.txt
```

## Installation

details

## Usage

A file with the metadata that needs to be used needs to be created in the config directory. Review one to see the fields required in detail.

The json should have the following root fields: 'scraper' and 'extractor'

The scraper field should have the following fields: 'url', 'allow_cookies_button'

The extractor field should have the following fields: 'output_filename', 'base_node' and 'child_nodes'

Within the child nodes, each node needs to have the following fields: 'find' which has the fields to find, and the 'return' which has the item to save.

Set the require config file's filename in your '.env' file in the root directory:

```
CONFIG_FILE=config_file_name.json
```

Then you can run the extractor with:

```
python src/main.py
```

## Testing

Testing is done with pytest and they will simply run with running pytest in the route directory.

`pytest`
