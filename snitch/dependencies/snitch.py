import dependencies.prefix as prefix
from dependencies.secrets import RegexSnitcher, EntropySnitcher, AISnitcher

from bs4 import BeautifulSoup
import requests

class SnitchResult:
    def __init__(self, location: str, method: str, type: str, secret: str) -> None:
        self.location: str = location
        self.method: str = method
        self.type: str = type
        self.secret: str = secret

class SnitchEngine:
    """
    This class is used to extract information from the content of a URL.
    """
    def __init__(self, content: requests.Response, verbose=False) -> None:
        self.content: requests.Response = content
        self.verbose: bool = verbose

    def extract_links(self) -> list[str]:
        """
        Exctract links from the content of the URL.
        """
        if self.verbose:
            print(f"{prefix.info} Extracting links from {prefix.cyan}{self.content.url}{prefix.reset}")

        return self.extract_urls_from_html()

    def extract_js(self) -> list[str]:
        """
        Extract JS from the content of the URL.
        """
        if self.verbose:
            print(f"{prefix.info} Extracting JS from {prefix.cyan}{self.content.url}{prefix.reset}")

        return self.extract_js_from_html()

    def extract_secrets(self, regex: bool=True, entropy: bool=True, entropy_threshold: float=4.5, char_limit: int=200, ai: bool=False, ai_threshold: float=0.9) -> dict:
        """
        Extract secrets from the content of the URL.
        """
        regex_secrets: list[tuple[str, str]] = []
        entropy_secrets: list[str] = []
        ai_secrets: list[str] = []

        if self.verbose:
            print(f"{prefix.info} Extracting secrets from {prefix.cyan}{self.content.url}{prefix.reset}")

        # Regex
        if regex:
            regex_snitcher = RegexSnitcher(self.content, verbose=self.verbose)
            regex_secrets = regex_snitcher.extract_secrets()
            regex_secrets = self.make_unique_list(regex_secrets)
        # Entropy
        if entropy:
            entropy_snitcher = EntropySnitcher(self.content, threshold=entropy_threshold, char_limit=char_limit, verbose=self.verbose)
            entropy_secrets = entropy_snitcher.extract_secrets()
            entropy_secrets = self.make_unique_list(entropy_secrets)
        # AI
        if ai:
            print(f"{prefix.warning} AI secret detection is experimental and may not work as expected.")
            print(f"{prefix.warning} Classification may take a long time based on content length.")
            ai_snitcher = AISnitcher(self.content, threshold=ai_threshold, verbose=self.verbose)
            ai_secrets = ai_snitcher.extract_secrets()
            ai_secrets = self.make_unique_list(ai_secrets)

        return {"regex": regex_secrets, "entropy": entropy_secrets, "ai": ai_secrets}

    def extract_urls_from_html(self):
        """
        Extract URLs from the content of the URL.
        """
        urls = []
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(self.content.text, "html.parser")
        for a in soup.find_all("a", href=True):
            # Skip external links
            if self.content.url not in a["href"]:
                # pass
                continue

            if self.verbose:
                print(f"{prefix.info} Found link: {prefix.cyan}{a['href']}{prefix.reset}")

            urls.append(a["href"])

        return urls

    def extract_js_from_html(self):
        urls = []
        soup = BeautifulSoup(self.content.text, "html.parser")

        for script in soup.find_all("script", src=True):
            url = script["src"]

            # Skip external scripts
            if url.startswith("http") or url.startswith("https"):
                continue

            # Check if the script URL is an absolute path
            if url.startswith("http://") or url.startswith("https://"):
                pass
            elif url.startswith("//"):
                url = self.content.url + url[2:] # remove leading //
            elif url.startswith("/"):
                url = self.content.url + url[1:] # remove leading /
            elif url.startswith("./"):
                url = self.content.url + url[2:] # remove leading ./
            else:
                url = self.content.url + url

            if self.verbose:
                print(f"{prefix.info} Found script: {prefix.yellow}{url}{prefix.reset}")

            urls.append(url)

        return urls

    def make_unique_list(self, target):
        """
        Remove duplicates from a list.
        """
        unique_list = []
        for item in target:
            if item in unique_list:
                continue
            unique_list.append(item)

        return unique_list
