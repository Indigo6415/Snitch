import dependencies.prefix as prefix
from dependencies.secrets import RegexSnitcher, EntropySnitcher

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import tldextract
import requests

import re


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
        self.hostname: str = self.get_main_domain(content.url)

    def extract_links(self) -> list[str]:
        """
        Exctract links from the content of the URL.
        """
        if self.verbose:
            print(
                f"{prefix.info} Extracting links from {prefix.cyan}{self.content.url}{prefix.reset}")

        return self.extract_urls_from_html()

    def extract_js(self) -> list[str]:
        """
        Extract JS from the content of the URL.
        """
        if self.verbose:
            print(
                f"{prefix.info} Extracting JS from {prefix.cyan}{self.content.url}{prefix.reset}")

        return self.extract_js_from_html()

    def extract_secrets(self, regex: bool = True, entropy: bool = True, entropy_threshold: float = 4.5, char_limit: int = 200, ai: bool = False, ai_threshold: float = 0.9) -> dict:
        """
        Extract secrets from the content of the URL.
        """
        regex_secrets: list[tuple[str, str]] = []
        entropy_secrets: list[str] = []
        ai_secrets: list[str] = []

        if self.verbose:
            print(
                f"{prefix.info} Extracting secrets from {prefix.cyan}{self.content.url}{prefix.reset}")

        # Regex
        if regex:
            regex_snitcher = RegexSnitcher(self.content, verbose=self.verbose)
            regex_secrets = regex_snitcher.extract_secrets()
            regex_secrets = self.make_unique_list(regex_secrets)
        # Entropy
        if entropy:
            entropy_snitcher = EntropySnitcher(
                self.content, threshold=entropy_threshold, char_limit=char_limit, verbose=self.verbose)
            entropy_secrets = entropy_snitcher.extract_secrets()
            entropy_secrets = self.make_unique_list(entropy_secrets)
        # AI
        # if ai:
        #     print(
        #         f"{prefix.warning} AI secret detection is experimental and may not work as expected.")
        #     print(
        #         f"{prefix.warning} Classification may take a long time based on content length.")
        #     ai_snitcher = AISnitcher(
        #         self.content, threshold=ai_threshold, verbose=self.verbose)
        #     ai_secrets = ai_snitcher.extract_secrets()
        #     ai_secrets = self.make_unique_list(ai_secrets)

        return {"regex": regex_secrets, "entropy": entropy_secrets, "ai": ai_secrets}

    def extract_urls_from_html(self):
        """
        Extract URLs from the content of the URL.
        """
        urls = []
        soup = BeautifulSoup(self.content.text, "html.parser")

        # Extract the main domain of the base URL
        base_domain = tldextract.extract(self.content.url).registered_domain

        for a in soup.find_all("a", href=True):
            link = a["href"]

            # Convert relative URLs to absolute
            link = urljoin(self.content.url, link)

            # Extract the main domain of the link
            link_domain = tldextract.extract(link).registered_domain

            # Skip external links (allow subdomains)
            if link_domain != base_domain:
                continue

                print(f"{prefix.info} Found link: {prefix.cyan}{link}{prefix.reset}")

            urls.append(link)

        regex_extracted_urls = self.extract_urls(self.content.text)
        # Check for cross-domain links
        for re_ex_url in regex_extracted_urls:
            link_domain = tldextract.extract(re_ex_url).registered_domain
            if re_ex_url != link_domain:
                continue
            if self.verbose:
                print(
                    f"{prefix.info} Found link: {prefix.cyan}{re_ex_url}{prefix.reset}")
            urls.append(re_ex_url)

        return urls

    def extract_urls(self, text):
        """
        Extracts all URLs from a given string.
        """
        url_pattern = re.compile(
            r'https?://[^\s<>"]+|www\.[^\s<>"]+|ftp://[^\s<>"]+|[a-zA-Z]+://[^\s<>"]+'
        )
        return url_pattern.findall(text)

    def extract_js_from_html(self):
        urls = []
        soup = BeautifulSoup(self.content.text, "html.parser")

        for script in soup.find_all("script", src=True):
            url = script["src"]

            # Skip external scripts
            if url.startswith("http") and self.hostname not in url or url.startswith("https") and self.hostname not in url:
                continue

            # Check if the script URL is an absolute path
            if url.startswith("http://") or url.startswith("https://"):
                pass
            elif url.startswith("//"):
                url = self.content.url + url[2:]  # remove leading //
            elif url.startswith("/"):
                url = self.content.url + url[1:]  # remove leading /
            elif url.startswith("./"):
                url = self.content.url + url[2:]  # remove leading ./
            else:
                url = self.content.url + url

            if self.verbose:
                print(
                    f"{prefix.info} Found script: {prefix.yellow}{url}{prefix.reset}")

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

    def get_main_domain(self, url: str) -> str:
        parsed_url = urlparse(url)
        extracted = tldextract.extract(parsed_url.netloc)
        return f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else f"{extracted.domain}"
