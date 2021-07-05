from website import app

import subprocess
import argparse

def netlify_deploy(alias, message):
    cmd = ["netlify", "deploy", "--alias", f"{alias}", "--dir", "website/build", "-m", f"{message}"]
    return subprocess.run(cmd)

def netlify_deploy_prod(message):
    cmd = ["netlify", "deploy", "--prod", "--dir", "website/build", "-m", f"{message}"]
    return subprocess.run(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Deploy website to netlify")
    parser.add_argument('-P', '--prod', action='store_true',
        help="Deploy into production")
    parser.add_argument('-A', '--alias', default='dev')
    parser.add_argument('-m', '--message', required=True)
    args = parser.parse_args()

    if args.prod:
        netlify_deploy_prod(args.message)

    elif args.alias:
        netlify_deploy(alias=args.alias, message=args.message)
