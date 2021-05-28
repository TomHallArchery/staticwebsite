import subprocess

def compile_css(src, dest, compressed=False, watch=False):
    cmnd = ["sass", f"{src}:{dest}", "--no-source-map"]
    if compressed:
        cmnd.extend([ "-s", "compressed"])
    if watch:
        cmnd.extend(['--watch'])
    res = subprocess.run(cmnd)
    return res
