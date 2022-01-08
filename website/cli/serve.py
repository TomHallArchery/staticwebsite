#!/usr/bin/env python
import http.server as svr
import multiprocessing

import click

from . import cli_bp as bp
from . import utils

ROOT_HEADERS = {
    'test_ROOT': "True",
    'Content-Security-Policy': """
    default-src 'self';
    script-src 'self' 'unsafe-eval';
    style-src 'self' 'unsafe-inline';
    font-src 'self';
    img-src 'self' localhost:5003;
    prefetch-src 'self' cdn.tomhallarchery.com;
    object-src 'none';
    frame-ancestors 'none';
    frame-src 'none';
    base-uri 'none'
      """,
    'Strict-Transport-Security': "max-age=63072000; includeSubDomains",
    'X-Frame-Options': "DENY",
    'X-Content-Type-Options': "nosniff",
    }

CDN_HEADERS = {
    'test_CDN': "True",
    # 'Content-Security-Policy' : """
    # default-src 'self';
    #   """,
    'Strict-Transport-Security': "max-age=63072000; includeSubDomains",
    'X-Frame-Options': "DENY",
    'X-Content-Type-Options': "nosniff",
    }


class MyReqHandler(svr.SimpleHTTPRequestHandler):
    ''' base custom request handler class '''


class ROOTReqHandler(MyReqHandler):
    ''' custom request handler to send root domain headers'''

    def end_headers(self):
        self.send_my_headers()
        super().end_headers()

    def send_my_headers(self):
        ''' override method to send custom headers '''
        for header, value in ROOT_HEADERS.items():
            self.send_header(header, value)

    def _error_page(self):
        with open('404.html', encoding="utf8") as f:
            return f.read()

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            print("Custom 404 handler")
            self.error_message_format = self._error_page()
        super().send_error(code, message, explain)


class CDNReqHandler(MyReqHandler):
    ''' custom request handler to send cdn domain headers'''

    def end_headers(self):
        self.send_my_headers()
        super().end_headers()

    def send_my_headers(self):
        ''' override method to send custom headers '''
        for header, value in CDN_HEADERS.items():
            self.send_header(header, value)


def serve_static(handler, directory, port):
    ''' serve static files from directory '''
    print("Serving: ", directory)
    with utils.cwd(directory):
        svr.test(HandlerClass=handler, port=port)


def serve_site():
    ''' serve frozen site on port 5002 '''
    serve_static(ROOTReqHandler, 'website/build', 5002)


def serve_cdn():
    ''' serve cdn on port 5003 '''
    serve_static(CDNReqHandler, 'website/static/img/out', 5003)


@bp.cli.command('serve')
def main():
    ''' serve from build directory and img '''
    proc1 = multiprocessing.Process(target=serve_site)
    proc2 = multiprocessing.Process(target=serve_cdn)
    proc1.start()
    proc2.start()


if __name__ == '__main__':
    main()
