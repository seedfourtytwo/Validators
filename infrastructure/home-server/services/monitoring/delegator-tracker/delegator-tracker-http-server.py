#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

class DelegatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Only serve the JSON data at the root path
        if self.path == '/':
            try:
                # Read the JSON file
                json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'delegators.json')
                with open(json_path, 'r') as f:
                    json_data = f.read()
                
                # Set response headers
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
                self.end_headers()
                
                # Send the JSON data
                self.wfile.write(json_data.encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Error reading JSON file: {str(e)}".encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

# Set up the server
server_address = ('', 8080)
httpd = HTTPServer(server_address, DelegatorHandler)
print("Server started at http://localhost:8080")
httpd.serve_forever() 