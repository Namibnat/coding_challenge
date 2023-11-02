"""Fetch, Extract and Save Routine"""


def async main():
    config = get_config()

    scrapper = Scraper()
    data = await scraper.get_data()

    extractor = None

