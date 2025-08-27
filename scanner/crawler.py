# scanner/crawler.py

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Crawler:
    """
    A simple crawler to discover forms and links on a webpage.
    In a real-world application, this would be far more complex, handling
    things like session management, JavaScript rendering, and respecting robots.txt.
    """
    
    def __init__(self, url: str):
        self.target_url = url
        self.session = requests.Session() # Use a session to persist cookies

    def get_forms(self) -> list:
        """Finds and returns all HTML forms on the page."""
        try:
            response = self.session.get(self.target_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.find_all('form')
        except requests.exceptions.RequestException as e:
            print(f"[Crawler] Error fetching {self.target_url}: {e}")
            return []

    def submit_form(self, form: BeautifulSoup, value: str) -> requests.Response:
        """
        Submits a given form with a provided value in all its text/search inputs.
        
        Args:
            form: A BeautifulSoup form object.
            value: The payload to inject into the form's input fields.

        Returns:
            The HTTP response after submitting the form.
        """
        action = form.get('action')
        post_url = urljoin(self.target_url, action)
        method = form.get('method').lower()

        inputs_list = form.find_all('input')
        post_data = {}
        for input_tag in inputs_list:
            input_name = input_tag.get('name')
            input_type = input_tag.get('type', 'text')
            input_value = input_tag.get('value', '')

            if input_type == 'text':
                post_data[input_name] = value # Inject our payload
            else:
                post_data[input_name] = input_value

        if method == 'post':
            return self.session.post(post_url, data=post_data)
        else: # Assumes GET
            return self.session.get(post_url, params=post_data)
