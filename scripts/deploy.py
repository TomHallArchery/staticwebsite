from website import app, utils
import config

app.config.from_object(config.DeployConfig)

if __name__ == '__main__':
    utils.deploy_folder_to_netlify('website/build', "ROOT")
    utils.deploy_folder_to_netlify('website/static/img/out', "CDN")
