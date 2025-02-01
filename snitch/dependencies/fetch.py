import requests
import dependencies.prefix as prefix
import os

class SnitchContent:
    """
    This class is a wrapper around the requests.Response object.
    It is used to provide a consistent interface for the Snitch
    application to interact with the requests.Response object.
    """
    def __init__(self, content: requests.Response) -> None:
        self.content: requests.Response = content

    def text(self) -> str:
        return self.content.text

    def status(self) -> int:
        return self.content.status_code

    def url(self) -> str:
        return self.content.url

    def headers(self) -> dict[str, str]:
        return dict(self.content.headers)

    def cookies(self) -> dict[str, str | None]:
        return {cookie.name: cookie.value for cookie in self.content.cookies}

    def size(self) -> int:
        return len(self.content.content)

    def describe(self) -> None:
        print(f"{prefix.info} Status: {self.status()}")
        print(f"{prefix.info} Size: {self.size()} bytes")

class FetchURL:
    """
    This class is used to fetch the content of a URL.
    """
    def __init__(self, url, use_headers=False, verbose=False) -> None:
        self.url = url
        self.verbose = verbose
        self.use_headers = use_headers
        self.headers = {
            "authority": "jwt.io",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.7",
            "cache-control": "max-age=0",
            "priority": "u=0, i",
            "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        }

    def fetch(self) -> SnitchContent | None:
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
            return SnitchContent(response)
        except Exception as e:
            print(f"{prefix.error} Error fetching content from {prefix.cyan}{self.url}{prefix.reset}")
            print(f"{prefix.error} {e}")
            os._exit(1)
