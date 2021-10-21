from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import data_handler


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        params = parse_qs(url.query)
        path = url.path
        
        if path == '/getSelectPageData':
            content = bytes(json.dumps(data_handler.get_select_page_data()), 'utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(content)
            return

        if path == '/getMainPageData':
            kreis = params["kreis"][0]
            content = bytes(json.dumps(data_handler.get_main_page_data(kreis)), 'utf-8')
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(content)
            return

        if path == '/':
            path = '/index.html'
        path = f"./content/{path[1:]}"

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
