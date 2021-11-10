from website import create_app
import config

app = create_app()
app.config.from_object(config.DevConfig)

if __name__ == '__main__':
    app.run()
