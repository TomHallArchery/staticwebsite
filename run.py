#!/usr/bin/env python
import subprocess
from time import sleep, localtime, strftime


from website import app, db, flatpages, utils, images


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

    # Extra debugging/testing functions
    pprint("LOG")
    with utils.cwd(images.IMAGES_ROOT):
        new_imgs, missing_imgs = images.check_img_dir('src')
        images.flag_new_imgs(new_imgs)
        images.proccess_new_imgs()

    # Run dev server
    app.run(debug=True)

    # Request to freeze
    sleep(0.5)
    freeze = input('Freeze application? (y/n): ')
    if freeze.lower() == 'y':
        cmd = ["python", "-m", "freeze"]
        subprocess.run(cmd)

    # clear database
    rundb.update({"Active": False})
    db.close()
