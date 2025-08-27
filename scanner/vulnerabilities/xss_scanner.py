# scanner/vulnerabilities/xss_scanner.py

from .base import VulnerabilityScanner
from scanner.crawler import Crawler # Import our new crawler

class XssScanner(VulnerabilityScanner):
    """
    Scans for Cross-Site Scripting (XSS) vulnerabilities.
    It uses the Crawler to find forms and injects a payload to test for reflections.
    """
    
    def scan(self, url: str) -> dict:
        result = {
            'vulnerability': 'Cross-Site Scripting (XSS)',
            'vulnerable': False,
            'details': 'No basic XSS vulnerabilities detected.'
        }
        
        # A simple, non-malicious payload to check for reflection.
        xss_test_script = "<script>alert('xss-test-payload')</script>"
        
        # The XssScanner uses the Crawler to do its discovery work.
        crawler = Crawler(url)
        forms = crawler.get_forms()

        if not forms:
            result['details'] = 'No forms found on the page to test for XSS.'
            return result

        for form in forms:
            try:
                response = crawler.submit_form(form, xss_test_script)
                # Check if our script is reflected in the response body.
                # This is a basic check; advanced tools would use a headless browser.
                if xss_test_script in response.text:
                    result['vulnerable'] = True
                    result['details'] = f"Reflected XSS vulnerability found in a form on {url}. Payload was successfully injected and reflected."
                    return result
            except Exception as e:
                # Silently ignore forms that fail to submit
                print(f"[XssScanner] Error submitting a form on {url}: {e}")
                continue
                
        return result
