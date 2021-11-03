#!/usr/bin/env python
import multiprocessing
from website import app, utils

def serve_site():
    utils.serve_static('website/build', 5002)

def serve_cdn():
    utils.serve_static('website/static/img/out', 5003)

def main():
    p1 = multiprocessing.Process(target=serve_site)
    p2 = multiprocessing.Process(target=serve_cdn)
    p1.start()
    p2.start()

if __name__ == '__main__':
    main()
