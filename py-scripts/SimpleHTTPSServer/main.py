#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import argparse
import base64
import html
import http.server
import io
import os
import socketserver
import ssl
import sys
import urllib
from http import HTTPStatus
from pathlib import Path
from time import gmtime

from OpenSSL import SSL, crypto

CERT_SAVE_DIR = str(Path(__file__).resolve().parent) + os.sep
CERT_PATH = rf"{CERT_SAVE_DIR}server.crt"
KEY_PATH = rf"{CERT_SAVE_DIR}server.key"
PEM_PATH = rf"{CERT_SAVE_DIR}server.pem"

USERNAME = 'admin'
PASSWORD = '123'
AUTH_KEY = base64.b64encode('{}:{}'.format(USERNAME, PASSWORD).encode()).decode()

def create_self_signed_cert(cert_path,key_path,pem_path):
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "UK"
    cert.get_subject().ST = "London"
    cert.get_subject().L = "London"
    cert.get_subject().O = "Dummy Company Ltd"
    cert.get_subject().OU = "Dummy Company Ltd"
    cert.get_subject().CN = socketserver.socket.gethostname()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')
    if not Path(cert_path).exists():
        open(cert_path, "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    if not Path(key_path).exists():
        open(key_path, "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    if not Path(pem_path).exists():
        open(pem_path, "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        open(pem_path, "ab").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    directory = None
    def __init__(self,*args,**kwargs):
        super().__init__(*args, directory=self.directory, **kwargs)
#        self.path = None or os.getcwd()
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="FileServer"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """ Present frontpage with user authentication. """
        if self.headers.get("Authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write(b"no auth header received")
        elif self.headers.get("Authorization") == "Basic " + AUTH_KEY:
            super().do_GET()
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.get("Authorization").encode())
            self.wfile.write(b"not authenticated")
    
 
    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(self.path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
#        title = f'Directory listing for {displaypath}'
        title = f'Directory listing for {self.directory}'
        r.append('<!DOCTYPE HTML>')
        r.append('<html lang="en">')
        r.append('<head>')
        r.append(f'<meta charset="{enc}">')
        r.append(f'<title>{title}</title>\n</head>')
        r.append(f'<body>\n<h1>{title}</h1>')
        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            r.append('<li><a href="%s">%s</a></li>'
                    % (urllib.parse.quote(linkname,
                                          errors='surrogatepass'),
                       html.escape(displayname, quote=False)))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f
        
    def translate_path(self, path):
        if self.directory:
            path = os.path.join(self.directory, path.lstrip('/'))
        return super().translate_path(path)
        
class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

def main():
    parser = argparse.ArgumentParser(description="SimpleHTTPSServer \n Usage: python3 SimpleHTTPSServer.py 443")
    parser.add_argument("--port", type=int, default=443, nargs="?", help="Port Number, default is 443")
    parser.add_argument("--dir", type=str, default=None, nargs="?", help="directory, default current")
    args = parser.parse_args()
    create_self_signed_cert(CERT_PATH,KEY_PATH,PEM_PATH)
    port = args.port
    address = ('0.0.0.0', port,)
    if port == 443:
        print(f'server listening at https://{address[0]} https://127.0.0.1')
    else:
        print(f'server listening at https://{address[0]}:{port} https://127.0.0.1:{port}')
    MyHandler.directory = args.dir
    with ThreadingHTTPServer(address, MyHandler) as httpd:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=PEM_PATH)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        httpd.serve_forever()

if __name__ == "__main__":
	main()