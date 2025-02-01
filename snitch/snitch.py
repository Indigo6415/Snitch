#!/usr/bin/env python3

from dependencies.snitch import SnitchEngine
from dependencies.fetch import FetchURL

verbose = True
url = "https://diep.io/"

def main():
    # Fetch the content of a URL
    content = FetchURL(url, verbose=verbose).fetch()

    # Extract links from the content
    snitch = SnitchEngine(content, verbose=verbose)
    snitch.extract_links()
    snitch.extract_js()

    # Extract secrets from the content
    # snitch.extract_secrets()


if __name__ == "__main__":
    # TODO: Create flag to save fetched content to disk.
    main()
