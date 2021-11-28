from website import create_app, utils
import config

app = create_app(config.DeployConfig)

if __name__ == '__main__':
    utils.deploy_folder_to_netlify(app, 'website/build', "ROOT")
    utils.deploy_folder_to_netlify(app, 'website/static/img/out', "CDN")
