#!/usr/bin/env python
from website import app, utils

def main():
    utils.serve_static('website/build', 5001)

if __name__ == '__main__':
    main()
