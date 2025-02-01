from dependencies.fetch import SnitchContent
import dependencies.prefix as prefix
from tqdm import tqdm

# Used for regex analysis
import re
# Used for entropy analysis
from collections import Counter
import math
# Used for AI analysis
from transformers import pipeline
import transformers
transformers.logging.set_verbosity_error() # Disable those stupid logs

class RegexSnitcher:
    def __init__(self, content: SnitchContent, verbose=False):
        self.content = content
        self.verbose = verbose
        self.patterns = {
            "AWS Access Key": r"AKIA[0-9A-Z]{12,20}",
            "AWS Secret Key": r"(?i)aws(.{0,20})?['\"][0-9a-zA-Z/+]{30,50}['\"]",
            "Google API Key": r"AIza[0-9A-Za-z-_]{25,35}",
            "Slack Token": r"xox[baprs]-([0-9a-zA-Z]{10,48})?",
            "JWT Token": r"eyJ[a-zA-Z0-9]{20,}\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",
            "Basic Auth": r"Basic [a-zA-Z0-9=:_\+/-]{5,100}",
            "Bearer Token": r"Bearer [a-zA-Z0-9-._~+/]{20,}",
            "MD5 Hash": r"\b[a-fA-F0-9]{32}\b",
            "SHA-1 Hash": r"\b[a-fA-F0-9]{40}\b",
            "SHA-256 Hash": r"\b[a-fA-F0-9]{64}\b",
            "SHA-512 Hash": r"\b[a-fA-F0-9]{128}\b",
        }

    def extract_secrets(self) -> dict[str, list[str]]:
        results = {}

        if self.verbose:
            print(f"{prefix.info} Extracting secrets using {prefix.magenta}regex{prefix.reset} from {prefix.cyan}{self.content.url()}{prefix.reset}")

        for key, pattern in self.patterns.items():
            matches = re.findall(pattern, self.content.text())
            if matches:
                results[key] = matches

        return results

class EntropySnitcher:
    def __init__(self, content: SnitchContent, verbose=False, threshold=4.5):
        self.content = content
        self.verbose = verbose
        self.threshold = threshold

    def extract_secrets(self) -> list[str]:
        if self.verbose:
            print(f"{prefix.info} Extracting secrets using {prefix.magenta}entropy{prefix.reset} from {prefix.cyan}{self.content.url()}{prefix.reset}")

        words = re.findall(r"[A-Za-z0-9+/=]{10,}", self.content.text())  # Extract words that look like keys
        return [word for word in words if self.shannon_entropy(word) > self.threshold]

    def shannon_entropy(self, string):
        """Calculate the entropy of a string"""
        p, lns = Counter(string), float(len(string))
        return -sum(count / lns * math.log2(count / lns) for count in p.values())

class AISnitcher:
    def __init__(self, content: SnitchContent, verbose=False, threshold=0.9):
        self.content = content
        self.verbose = verbose
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.labels = ["secret", "public"]
        self.threshold = threshold

    def extract_secrets(self) -> list[str]:
        results = []
        if self.verbose:
            print(f"{prefix.info} Extracting secrets using {prefix.magenta}AI{prefix.reset} from {prefix.cyan}{self.content.url()}{prefix.reset}")

        for line in tqdm(self.content.text().split("\n"), desc="Processing lines"):
            if line.strip() == "":
                continue
            verdict: dict = dict(self.classifier(line, self.labels))
            index = verdict["labels"].index("secret")
            if verdict["scores"][index] > self.threshold:
                results.append(line)
                print(verdict)


        return results
