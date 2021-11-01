from website import app, utils
import config

app.config.from_object(config.BuildConfig)

if __name__ == '__main__':
    utils.deploy_folder_to_netlify('website/build', "ROOT")
