import requests
from .base import VulnerabilityScanner

class ClickjackingScanner(VulnerabilityScanner):
    """
    Scans for Clickjacking vulnerability by checking HTTP security headers.
    """
    
    def scan(self, url: str) -> dict:
        result = {
            'vulnerability': 'Clickjacking',
            'vulnerable': False,
            'details': 'No Clickjacking vulnerability detected.'
        }
        
        try:
            response = requests.get(url, timeout=10)
            headers = response.headers
            
            # Modern browsers prioritize CSP frame-ancestors
            csp_header = headers.get('Content-Security-Policy', '')
            if 'frame-ancestors' in csp_header:
                if "'none'" in csp_header or "'self'" in csp_header:
                    result['details'] = 'Site is protected by Content-Security-Policy (frame-ancestors).'
                    return result
            
            # Check for the legacy X-Frame-Options header
            x_frame_options = headers.get('X-Frame-Options', '').lower()
            if x_frame_options in ['deny', 'sameorigin']:
                result['details'] = f"Site is protected by X-Frame-Options: {x_frame_options.upper()}."
                return result

            # If neither protective header is properly set, it's vulnerable
            result['vulnerable'] = True
            result['details'] = 'The application is missing the X-Frame-Options and Content-Security-Policy (frame-ancestors) headers, making it vulnerable to Clickjacking.'

        except requests.exceptions.RequestException as e:
            result['vulnerable'] = False # Can't determine, so assume not vulnerable
            result['details'] = f"Could not connect to the URL: {e}"
            
        return result
