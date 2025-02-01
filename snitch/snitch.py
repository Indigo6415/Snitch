#!/usr/bin/env python3

from dependencies.snitch import SnitchEngine
from dependencies.fetch import FetchURL

verbose = False
use_headers = False
url = "https://www.nytimes.com"
# url = "http://localhost:9999/index.html"

def main():
    # Fetch the content of a URL
    content = FetchURL(url, use_headers=use_headers, verbose=verbose).fetch()

    # Extract links from the content
    snitch = SnitchEngine(content, verbose=verbose)
    snitch.extract_links()
    snitch.extract_js()

    # Extract secrets from the content
    snitch.extract_secrets(regex=True, entropy=True, entropy_threshold=4.5, ai=False, ai_threshold=0.9)


if __name__ == "__main__":
    # TODO: Create flag to save fetched content to disk.
    main()
