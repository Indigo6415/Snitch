import dependencies.prefix as prefix
from dependencies.fetch import SnitchContent
from dependencies.secrets import RegexSnitcher, EntropySnitcher, AISnitcher

from bs4 import BeautifulSoup

class SnitchEngine:
    def __init__(self, content: SnitchContent, verbose=False) -> None:
        self.content: SnitchContent = content
        self.verbose: bool = verbose

    def extract_links(self) -> list[str]:
        if self.verbose:
            print(f"{prefix.info} Extracting links from {prefix.cyan}{self.content.url()}{prefix.reset}")

        return self.extract_urls_from_html()

    def extract_js(self) -> list[str]:
        if self.verbose:
            print(f"{prefix.info} Extracting JS from {prefix.cyan}{self.content.url()}{prefix.reset}")

        return self.extract_js_from_html()

    def extract_secrets(self, regex: bool=True, entropy: bool=True, entropy_threshold: float=4.5, ai: bool=False, ai_threshold: float=0.9) -> None:
        if self.verbose:
            print(f"{prefix.info} Extracting secrets from {prefix.cyan}{self.content.url()}{prefix.reset}")

        # Regex
        if regex:
            regex_snitcher = RegexSnitcher(self.content, verbose=self.verbose)
            print(regex_snitcher.extract_secrets())
        # Entropy
        if entropy:
            entropy_snitcher = EntropySnitcher(self.content, verbose=self.verbose)
            print(entropy_snitcher.extract_secrets())
        # AI
        if ai:
            print(f"{prefix.warning} AI secret detection is experimental and may not work as expected.")
            print(f"{prefix.warning} Classification may take a long time based on content length.")
            ai_snitcher = AISnitcher(self.content, verbose=self.verbose)
            print(ai_snitcher.extract_secrets())

    def extract_urls_from_html(self):
        urls = []
        soup = BeautifulSoup(self.content.text(), "html.parser")
        for a in soup.find_all("a", href=True):
            # Skip external links
            if self.content.url() not in a["href"]:
                continue

            if self.verbose:
                print(f"{prefix.info} Found link: {prefix.cyan}{a['href']}{prefix.reset}")

            urls.append(a["href"])

        return urls

    def extract_js_from_html(self):
        urls = []
        soup = BeautifulSoup(self.content.text(), "html.parser")

        for script in soup.find_all("script", src=True):
            url = script["src"]

            # Skip external scripts
            if url.startswith("http") or url.startswith("https"):
                continue

            # Check if the script URL is an absolute path
            if url.startswith("http://") or url.startswith("https://"):
                pass

            # Append the URL of the website to the script URL
            elif url.startswith("//"):
                url = self.content.url() + url[2:] # remove leading //
            elif url.startswith("/"):
                url = self.content.url() + url[1:] # remove leading /
            elif url.startswith("./"):
                url = self.content.url() + url[2:] # remove leading ./
            else:
                if self.content.url().endswith("/"):
                    url = self.content.url() + url
                else:
                    url = self.content.url() + "/" + url

            if self.verbose:
                print(f"{prefix.info} Found script: {prefix.yellow}{url}{prefix.reset}")

            urls.append(url)

        return urls
