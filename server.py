from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path == '/api':
            content = bytes(f"API", 'utf-8')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(content)
            return

        if path == '/':
            path = '/index.html'
        path = f"content\{path[1:]}"

        try:
            with open(path, "rb") as reader:
                content = reader.read()
            self.send_response(200)
        except:
            content = bytes(f"{path} : File not found", 'utf-8')
            self.send_response(404)
        self.end_headers()
        self.wfile.write(content)

    '''
    def getQuery(self) -> dict:
        query = urlparse(self.path).query
        return dict(qc.split("=") for qc in query.split("&"))
    '''


httpd = HTTPServer(('localhost', 8080), ServerHandler)
httpd.serve_forever()
