import time

import requests
import signal
import sys
import urllib.parse
import ast
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

SECONDS_IN_DAY = 86400  # Seconds in one day
SECONDS_IN_MONTH = 30 * SECONDS_IN_DAY  # Seconds in a month


class Storage:
    def __init__(self):
        self.cache = {}

    def add_to_cache(self, key, value, ttl_month=1):
        """Adds value to cache with a key."""
        ttl_seconds = ttl_month * SECONDS_IN_MONTH
        self.cache[key] = {'value': value, 'expiry_time': time.time() + ttl_seconds}

    def delete_partner(self, key):
        """Deletes value from cache by the key."""
        if key in self.cache:
            del self.cache[key]

    def read_cache(self, key):
        """Returns cache value by the key."""
        if key in self.cache:
            if time.time() < self.cache[key]['expiry_time']:
                return self.cache[key]['value']
        else:
            del self.cache[key]
        return None


class ProjectProxy:
    def __init__(self):
        self.shutdown_requested = False

    def start_server(self):
        class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.0"

            def do_GET(self):
                self._handle_request("get", requests.get)

            def do_DELETE(self):
                self._handle_request("delete", requests.delete)

            def do_POST(self):
                self._handle_request("post", requests.post)

            def do_PUT(self):
                self._handle_request("put", requests.put)

            def do_PATCH(self):
                self._handle_request("patch", requests.patch)

            def _handle_request(self, method, requests_func):
                url = self._resolve_url()

                if url is None:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    return

                try:
                    content_length = int(self.headers["content-length"])
                    body = self.rfile.read(content_length).decode('UTF-8')
                    body = ast.literal_eval(body)
                    del body['id']

                    headers = dict(self.headers)
                    resp = requests_func(url, data=body, headers=headers)

                    self.send_response(resp.status_code)
                    self.end_headers()
                    self.wfile.write(resp.content)

                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-Type", "text/plain")
                    self.end_headers()
                    self.wfile.write(str(e).encode())

            def _resolve_url(self):
                parts = urllib.parse.urlparse(self.path)

                # get path without uuid in it
                rx = re.compile(r'\b[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}\b')
                parts._replace(path=re.sub(rx, '', parts.path))

                return parts.geturl()


        server_address = ('', 8000)
        self.httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
        self._register_signals()
        self.httpd.serve_forever()

    def _register_signals(self):
        signal.signal(signal.SIGTERM, self._shutdown_handler)
        signal.signal(signal.SIGINT, self._shutdown_handler)

    def _shutdown_handler(self, signum, frame):
        print("Shutting down gracefully...")
        self.shutdown_requested = True
        self.httpd.shutdown()

if __name__ == '__main__':
    proxy = ProjectProxy()
    proxy.start_server()
