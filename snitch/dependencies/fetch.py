import requests
import dependencies.prefix as prefix
import os

class SnitchContent:
    """
    This class is a wrapper around the requests.Response object.
    It is used to provide a consistent interface for the Snitch
    application to interact with the requests.Response object.
    """
    def __init__(self) -> None:
        self.new_links: list[str] = [] # List of new links found in the content
        self.extracted_links: list[str] = [] # List of links extracted from the content
        self.extracted_content: list[tuple[str, requests.Response]] = [] # List of content extracted from the URL

    def add_new_link(self, link: str | list) -> None:
        if type(link) is str:
            # Check if the link is already in the new_links list
            if link not in self.new_links:
                self.new_links.append(link)

        if type(link) is list:
            for candidate in link:
                # Check if the link is already in the new_links list
                if candidate not in self.new_links:
                    self.new_links.append(candidate)

    def add_extracted_link(self, link: str) -> None:
        if link not in self.extracted_links:
            self.extracted_links.append(link)

    def add_extracted_content(self, content: tuple) -> None:
        if content not in self.extracted_content:
            self.extracted_content.append(content)

    def merge_new_and_extracted_links(self) -> None:
        for link in self.new_links:
            self.add_extracted_link(link)

    def clear_new_links(self) -> None:
        self.new_links.clear()



class FetchURL:
    """
    This class is used to fetch the content of a URL.
    """
    def __init__(self, url, use_headers=False, verbose=False) -> None:
        self.url = url
        self.verbose = verbose
        self.use_headers = use_headers
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.7",
            "cache-control": "max-age=0",
            "priority": "u=0, i",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"MacOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }

    def fetch(self) -> requests.Response | None:
        if self.verbose:
            print(f"{prefix.info} Fetching content from {prefix.cyan}{self.url}{prefix.reset}")

        # Fetch content from the URL
        try:
            if self.use_headers:
                response = requests.get(self.url, headers=self.headers)
            else:
                response = requests.get(self.url)
            # Check if the request was successful
            if response.status_code != 200:
                print(f"{prefix.error} Error fetching content from {prefix.cyan}{self.url}{prefix.reset}")
                print(f"{prefix.error} Status code: {response.status_code}")
                return None

            print(f"{prefix.ok} Successfully fetched content from {prefix.cyan}{self.url}{prefix.reset}")
            return response
        except Exception as e:
            print(f"{prefix.error} Error fetching content from {prefix.cyan}{self.url}{prefix.reset}")
            print(f"{prefix.error} {e}")
            os._exit(1)
