from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

# Import our scanners
from scanner.vulnerabilities.clickjacking_scanner import ClickjackingScanner
from scanner.vulnerabilities.directory_traversal_scanner import DirectoryTraversalScanner

app = Flask(__name__)
# Enable CORS to allow our T3 frontend (on a different port) to call this API
CORS(app) 

# --- Dependency Injection and Service Registration ---
# This is where we register all the scanners our application knows about.
# Adheres to the Open/Closed Principle: to add a new scan, just add the class here.
VULNERABILITY_SCANNERS = [
    ClickjackingScanner(),
    DirectoryTraversalScanner(),
    # Add future scanners (XSS, SQLi) here...
]

@app.route('/api/scan', methods=['POST'])
def scan_url():
    """
    API endpoint to handle scan requests.
    Expects a JSON body with a "url" key.
    """
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required in the JSON body.'}), 400
    
    url = data['url']
    
    # --- Orchestration Layer ---
    results = []
    for scanner in VULNERABILITY_SCANNERS:
        # The app.py doesn't care *how* the scan is done, only that it *can* be done.
        # This respects the Liskov Substitution Principle.
        results.append(scanner.scan(url))
    
    return jsonify({
        'scanUrl': url,
        'results': results
    })

if __name__ == '__main__':
    # The backend will run on port 5001 to avoid conflicts with the frontend
    app.run(port=5001, debug=True)
