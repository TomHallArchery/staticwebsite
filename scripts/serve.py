#!/usr/bin/env python
import multiprocessing
import http.server as svr

from website import utils

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


class ROOT_HTTPReqHandler(svr.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        super().end_headers()

    def send_my_headers(self):
        for header, value in ROOT_HEADERS.items():
            self.send_header(header, value)


class CDN_HTTPReqHandler(svr.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        super().end_headers()

    def send_my_headers(self):
        for header, value in CDN_HEADERS.items():
            self.send_header(header, value)


def serve_static(handler, dir, port):
    print("Serving: ", dir)
    with utils.cwd(dir):
        svr.test(HandlerClass=handler, port=port)


def serve_site():
    serve_static(ROOT_HTTPReqHandler, 'website/build', 5002)


def serve_cdn():
    serve_static(CDN_HTTPReqHandler, 'website/static/img/out', 5003)


def main():
    p1 = multiprocessing.Process(target=serve_site)
    p2 = multiprocessing.Process(target=serve_cdn)
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()
