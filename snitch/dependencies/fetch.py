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

class FetchURL:
    """
    This class is used to fetch the content of a URL.
    """
    def __init__(self, url, verbose=False) -> None:
        self.url = url
        self.verbose = verbose

    def fetch(self) -> SnitchContent:
        if self.verbose:
            print(f"{prefix.info} Fetching content from {prefix.cyan}{self.url}{prefix.reset}")

        # Fetch content from the URL
        try:
            response = requests.get(self.url)
            # Check if the request was successful
            if response.status_code != 200:
                print(f"{prefix.error} Error fetching content from {prefix.cyan}{self.url}{prefix.reset}")
                print(f"{prefix.error} Status code: {response.status_code}")
                os._exit(1)

            print(f"{prefix.ok} Successfully fetched content from {prefix.cyan}{self.url}{prefix.reset}")
            return SnitchContent(response)
        except Exception as e:
            print(f"{prefix.error} Error fetching content from {prefix.cyan}{self.url}{prefix.reset}")
            print(f"{prefix.error} {e}")
            os._exit(1)
