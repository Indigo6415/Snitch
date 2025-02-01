import dependencies.prefix as prefix
from dependencies.fetch import SnitchContent

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

    def extract_secrets(self) -> None:
        if self.verbose:
            print(f"{prefix.info} Extracting secrets from {prefix.cyan}{self.content.url()}{prefix.reset}")

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
            # Skip external scripts
            if script["src"].startswith("http") or script["src"].startswith("https"):
                continue

            # Check if the script URL is an absolute path
            if script["src"].startswith("http://") or script["src"].startswith("https://"):
                pass
            # Append the URL of the website to the script URL
            elif script["src"].startswith("/"):
                script["src"] = self.content.url() + script["src"][1:]
            elif script["src"].startswith("./"):
                script["src"] = self.content.url() + script["src"][2:]
            else:
                script["src"] = self.content.url() + script["src"]

            if self.verbose:
                print(f"{prefix.info} Found script: {prefix.yellow}{script['src']}{prefix.reset}")

            urls.append(script["src"])

        return urls
