# scanner/vulnerabilities/sqli_scanner.py

from .base import VulnerabilityScanner
from scanner.crawler import Crawler
import time

class SqliScanner(VulnerabilityScanner):
    """
    Scans for SQL Injection vulnerabilities using error-based and time-based detection.
    """
    
    def scan(self, url: str) -> dict:
        result = {
            'vulnerability': 'SQL Injection',
            'vulnerable': False,
            'details': 'No SQL Injection vulnerabilities detected.'
        }
        
        # Common SQLi test payloads
        error_payloads = ["'", '"', "1' OR '1'='1"]
        time_payload = "1' AND SLEEP(3)--"
        
        crawler = Crawler(url)
        forms = crawler.get_forms()

        if not forms:
            result['details'] = 'No forms found on the page to test for SQL Injection.'
            return result

        # Test for error-based SQLi
        for form in forms:
            for payload in error_payloads:
                try:
                    response = crawler.submit_form(form, payload)
                    # Look for database error messages
                    error_indicators = [
                        "mysql_fetch_array", "ORA-", "Microsoft OLE DB",
                        "error in your SQL syntax", "SQLite error"
                    ]
                    
                    for indicator in error_indicators:
                        if indicator.lower() in response.text.lower():
                            result['vulnerable'] = True
                            result['details'] = f"SQL Injection vulnerability detected. Database error revealed with payload: '{payload}'"
                            return result
                            
                except Exception as e:
                    continue

        # Test for time-based SQLi (simplified)
        for form in forms:
            try:
                start_time = time.time()
                response = crawler.submit_form(form, time_payload)
                elapsed_time = time.time() - start_time
                
                if elapsed_time > 3:  # If response took longer than 3 seconds
                    result['vulnerable'] = True
                    result['details'] = f"Time-based SQL Injection vulnerability detected. Response delayed by {elapsed_time:.2f} seconds."
                    return result
                    
            except Exception as e:
                continue
                
        return result
