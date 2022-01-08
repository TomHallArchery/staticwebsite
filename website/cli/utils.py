import os
import subprocess
from contextlib import contextmanager


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def compile_css(app, compressed=False, watch=False):
    ''' launch subprocess to run dart sass '''
    source = app.config["CSS_SRC_DIR"]
    dest = app.config["CSS_OUT_DIR"]
    cmnd = ["sass", f"{source}:{dest}", "--no-source-map"]
    if compressed:
        cmnd.extend(["-s", "compressed"])
    if watch:
        cmnd.extend(['--watch'])
    res = subprocess.Popen(cmnd)
    return res
