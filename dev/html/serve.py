import http.server as svr
import subprocess

cmnd = ["sass", "scss:css", "--no-source-map"]
res = subprocess.run(cmnd)
print(res)
svr.test(HandlerClass=svr.SimpleHTTPRequestHandler, port=8080)
