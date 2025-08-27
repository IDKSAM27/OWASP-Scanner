# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from scanner.vulnerabilities.clickjacking_scanner import ClickjackingScanner
from scanner.vulnerabilities.xss_scanner import XssScanner
from scanner.vulnerabilities.directory_traversal_scanner import DirectoryTraversalScanner
from scanner.vulnerabilities.sqli_scanner import SqliScanner

app = Flask(__name__)
CORS(app)

# Change this route to match what your frontend is calling
@app.route('/api/scan', methods=['POST'])
def scan_url():
    """API endpoint to handle scan requests."""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required in the request body.'}), 400

    url = data['url']

    # Orchestration Layer
    scanners_to_run = [
        ClickjackingScanner(),
        XssScanner(),
        DirectoryTraversalScanner(),
        SqliScanner(),
    ]
    
    results = []
    for scanner in scanners_to_run:
        try:
            result = scanner.scan(url)
            results.append(result)
        except Exception as e:
            # Handle individual scanner failures gracefully
            results.append({
                'vulnerability': scanner.__class__.__name__,
                'vulnerable': False,
                'details': f'Scanner error: {str(e)}'
            })
    
    return jsonify({'url': url, 'results': results})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
