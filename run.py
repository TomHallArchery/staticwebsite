#!/usr/bin/env python

from website import app, db, qr, flatpages, utils, images
import subprocess
from time import sleep, localtime, strftime

app.config['ENV'] = 'DEVELOPMENT'
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

IMAGES_URL = "/static/img/out/"

rundb = db.table("run")

#Test dynamic database value insertion
TESTDBVAL = strftime("%X %x", localtime())
rundb.update({"Active": True, "Started": TESTDBVAL})



def pprint(string):
    print(string.center(30, "*"))

# recompile scss on each request during development mode
@app.before_request
def rebuild_css():
    utils.compile_css('website/static/scss', 'website/static/css')

# overload img_url with relative url to same domain
@app.context_processor
def localise_img_url():
    return dict(
        img_url=IMAGES_URL,
        )

if __name__ == '__main__':

    utils.clean_flatpage_metas(flatpages)

    rebuild_css()

    pprint("LOG")
    app.run(debug=True)
    sleep(0.5)

    freeze = input('Freeze application? (y/n): ')
    if freeze.lower() == 'y':
        cmd = ["python", "-m", "freeze"]
        subprocess.run(cmd)

    rundb.update({"Active": False})
