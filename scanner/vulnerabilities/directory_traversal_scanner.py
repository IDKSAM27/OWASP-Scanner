# scanner/vulnerabilities/directory_traversal_scanner.py

import requests
from urllib.parse import urljoin
from .base import VulnerabilityScanner

class DirectoryTraversalScanner(VulnerabilityScanner):
    """
    Scans for Directory Traversal vulnerabilities by attempting to access sensitive files.
    
    Note: This is a basic implementation. A professional tool would use a much
    larger and more sophisticated list of payloads and detection methods.
    """

    def __init__(self):
        # A small list of common payloads for demonstration
        self.payloads = [
            "../../../../etc/passwd",
            "../../../../boot.ini",
        ]

    def scan(self, url: str) -> dict:
        result = {
            'vulnerability': 'Directory Traversal',
            'vulnerable': False,
            'details': 'No Directory Traversal vulnerability detected.'
        }

        # This check is simplified. A real scanner would first crawl the site
        # to find parameters that look like they accept filenames.
        # For this example, we will assume a common parameter `file=`.
        param_to_test = "file" 

        for payload in self.payloads:
            test_url = f"{url}?{param_to_test}={payload}"
            try:
                response = requests.get(test_url, timeout=10)
                # Check for common signs of success in the response content
                if "root:x:0:0" in response.text or "[boot loader]" in response.text:
                    result['vulnerable'] = True
                    result['details'] = f"Vulnerability detected with payload: '{payload}'. The server responded with sensitive file content."
                    # On first detection, we can stop and report.
                    return result
            except requests.exceptions.RequestException:
                # Ignore connection errors and continue to the next payload
                continue
                
        return result
