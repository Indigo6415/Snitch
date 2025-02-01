#!/usr/bin/env python3

from dependencies.snitch import SnitchEngine
from dependencies.fetch import FetchURL, SnitchContent
import dependencies.prefix as prefix

verbose = False
use_headers = False
recursion_depth = 1
url = "https://wappalyzer.com/"
# url = "http://localhost:9999/index.html"
if not url.endswith("/"):
    url += "/"

def main():
    extracted_secrets: dict = {"filtered": [], "unfiltered": []}
    extracted_content: list[SnitchContent] = []
    extracted_links: list[str] = []
    extracted_links.append(url)
    new_links: list[str] = []
    new_links.append(url)

    for recursion in range(0, recursion_depth + 1):
        # Make room for the new new links, not the old links.
        temp_new_links = new_links.copy()
        new_links.clear()

        # Clear the temp links so that they can be filled again.
        # Only fetch the content of the URL if it has not been fetched before.
        for link in temp_new_links:
            if verbose: print("="*50)

            # Fetch the content of a URL
            content = FetchURL(link, use_headers=use_headers, verbose=verbose).fetch()
            if not content:
                continue
            content.describe()
            extracted_content.append(content)

            snitch_engine = SnitchEngine(content, verbose=verbose)

            # Extract links from the content
            links = snitch_engine.extract_links()
            new_links.extend(links)
            extracted_links.extend(links)
            if not links and verbose:
                print(f"{prefix.warning} No links found in {prefix.cyan}{content.url()}{prefix.reset}")

            # Extract JS from the content
            js = snitch_engine.extract_js()
            new_links.extend(js)
            extracted_links.extend(js)
            if not new_links and verbose:
                print(f"{prefix.warning} No JavaScript files found in {prefix.cyan}{content.url()}{prefix.reset}")

    # Remove any duplicates from the extracted content
    unique_content: list[SnitchContent] = []
    for content in extracted_content:
        if content in unique_content:
            continue
        unique_content.append(content)

    if verbose: print("="*50)

    # Extract secrets from the content
    for content in unique_content:
        snitch_engine = SnitchEngine(content, verbose=False)

        # Extract secrets from the content
        secrets = snitch_engine.extract_secrets(regex=True, entropy=True, entropy_threshold=4.5, char_limit=200, ai=False, ai_threshold=0.9)
        extracted_secrets["filtered"].extend(secrets["regex"].values())
        extracted_secrets["unfiltered"].extend(secrets["entropy"])
        extracted_secrets["unfiltered"].extend(secrets["ai"])

    # Remove any duplicates from the extracted secrets
    # unique_secrets: list = []
    # for content in extracted_secrets:
    #     if content in unique_secrets:
    #         continue
    #     unique_secrets.append(content)

    print(extracted_secrets)

    # for secret in extracted_secrets:
    #     print(secret.value())



if __name__ == "__main__":
    # TODO: Create flag to save fetched content to disk.
    main()
