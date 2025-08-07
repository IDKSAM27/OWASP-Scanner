from abc import ABC, abstractmethod

class VulnerabilityScanner(ABC):
    """
    Abstract base class for a vulnerability scanner.
    Defines the contract that all specific vulnerability scanners must follow.
    """
    
    @abstractmethod
    def scan(self, url: str) -> dict:
        """
        Runs the scan for a specific vulnerability on the given URL.

        Args:
            url: The target URL to scan.

        Returns:
            A dictionary containing the results of the scan.
            Example: {'vulnerable': True, 'details': 'X-Frame-Options header not set.'}
        """
        pass

