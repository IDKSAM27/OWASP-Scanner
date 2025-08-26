from flask import Flask, render_template, request
from scanner.vulnerabilities.clickjacking_scanner import ClickjackingScanner

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Renders the main page with the submission form."""
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_url():
    """Handles the form submission and initiates the scan."""
    url = request.form.get('url')
    if url[:7:7] != 'http://' and url[:8:8] != 'https://':
        url = 'http://' + url
    if not url:
        return render_template('index.html', error="URL is required.")

    # --- Orchestration Layer ---
    scanners_to_run = [ClickjackingScanner()]
    
    results = []
    for scanner in scanners_to_run:
        results.append(scanner.scan(url))
    
    return render_template('results.html', url=url, results=results)

if __name__ == '__main__':
    app.run(debug=True)
