import dependencies.prefix as prefix
from tqdm import tqdm
import requests

# Used for regex analysis
import dependencies.regex_patterns as regex_patterns
import re
# Used for entropy analysis
from collections import Counter
import math
# Used for AI analysis
from transformers import pipeline
import transformers
transformers.logging.set_verbosity_error() # Disable those stupid logs

class RegexSnitcher:
    def __init__(self, content: requests.Response, verbose=False):
        self.content = content
        self.verbose = verbose
        self.patterns = regex_patterns.keys

    def extract_secrets(self) -> list[tuple[str, str]]:
        results = []

        if self.verbose:
            print(f"{prefix.info} Extracting secrets using {prefix.magenta}regex{prefix.reset} from {prefix.cyan}{self.content.url}{prefix.reset}")

        for key, pattern in self.patterns.items():
            matches = re.findall(pattern, self.content.text)
            for match in matches:
                results.append((key, match))  # Append as tuple (key, match)

        return results

class EntropySnitcher:
    def __init__(self, content: requests.Response, verbose=False, threshold=4.5, char_limit=200):
        self.content = content
        self.verbose = verbose
        self.threshold = threshold
        self.char_limit = char_limit

    def extract_secrets(self) -> list[str]:
        if self.verbose:
            print(f"{prefix.info} Extracting secrets using {prefix.magenta}entropy{prefix.reset} from {prefix.cyan}{self.content.url}{prefix.reset}")

        words = re.findall(r"[A-Za-z0-9+/=]{10,}", self.content.text)  # Extract words that look like keys
        return [word for word in words if self.shannon_entropy(word) > self.threshold and len(word) < self.char_limit]

    def shannon_entropy(self, string):
        """Calculate the entropy of a string"""
        p, lns = Counter(string), float(len(string))
        return -sum(count / lns * math.log2(count / lns) for count in p.values())

class AISnitcher:
    def __init__(self, content: requests.Response, verbose=False, threshold=0.9):
        self.content = content
        self.verbose = verbose
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.labels = ["secret", "public"]
        self.threshold = threshold

    def extract_secrets(self) -> list[str]:
        results = []
        if self.verbose:
            print(f"{prefix.info} Extracting secrets using {prefix.magenta}AI{prefix.reset} from {prefix.cyan}{self.content.url}{prefix.reset}")

        for line in tqdm(self.content.text.split("\n"), desc="Processing lines"):
            if line.strip() == "":
                continue
            verdict: dict = dict(self.classifier(line, self.labels))
            index = verdict["labels"].index("secret")
            if verdict["scores"][index] > self.threshold:
                results.append(line)
                print(verdict)


        return results
