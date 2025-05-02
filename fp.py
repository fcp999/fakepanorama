from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote

class FakePanoramaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)

        body = b"""
<response status="error">
  <msg><line>Invalid request</line></msg>
</response>
"""

        if query.get('type') == ['keygen']:
            body = b"""
<response status="success">
  <result>
    <key>FAKEKEY1234567890abcdef</key>
  </result>
</response>
"""

        elif query.get('type') == ['config'] and query.get('action') == ['set']:
            xpath = unquote(query.get('xpath', [''])[0])
            element = unquote(query.get('element', [''])[0])
            print(f"[SET] xpath: {xpath}\n[SET] element: {element}")
            body = b"""
<response status="success">
  <msg>
    <line>command succeeded</line>
  </msg>
</response>
"""

        elif query.get('type') == ['config'] and query.get('action') == ['move']:
            xpath = unquote(query.get('xpath', [''])[0])
            where = query.get('where', [''])[0]
            dst = query.get('dst', [''])[0]
            print(f"[MOVE] xpath: {xpath}\n[MOVE] where: {where}\n[MOVE] dst: {dst}")
            body = b"""
<response status="success">
  <msg>
    <line>command succeeded</line>
  </msg>
</response>
"""

        elif query.get('type') == ['commit']:
            cmd = unquote(query.get('cmd', [''])[0])
            print(f"[COMMIT] cmd: {cmd}")
            body = b"""
<response status="success">
  <msg>
    <line>Commit job enqueued with jobid 42</line>
  </msg>
  <result>
    <job>42</job>
  </result>
</response>
"""

        elif query.get('type') == ['config'] and query.get('action') == ['get']:
            xpath = query.get('xpath', [''])[0]
            if xpath == "/config/devices/entry/device-group/entry/@name":
                body = b"""
<response status="success">
  <result>
    <entry name="Lab-Firewalls"/>
    <entry name="Production-FWs"/>
  </result>
</response>
"""
            else:
                body = b"""
<response status="error">
  <msg><line>Unsupported XPath</line></msg>
</response>
"""

        self.send_response(200)
        self.send_header('Content-Type', 'text/xml')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(body)
        self.wfile.flush()

def run(server_class=HTTPServer, handler_class=FakePanoramaHandler, port=8081):
    server = server_class(('', port), handler_class)
    print(f'Serving fake Panorama on port {port}...')
    server.serve_forever()

if __name__ == '__main__':
    run()

