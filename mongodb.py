import os
from dotenv import load_dotenv
import mongoengine as mg
from datetime import datetime

load_dotenv()

mg.connect('website', #connects to website DB
            username="app",
            password=os.environ.get("DB_PWORD"),
            authentication_source="admin",
            port=5009)

# creates or loads collection
class Img(mg.Document):
    name = mg.StringField()
    desc = mg.StringField()
    created_at = mg.DateTimeField()

class Page(mg.Document):
    title = mg.StringField()
    content = mg.StringField()

a = Img(name="img_1", desc="test img database", created_at=datetime.now()).save()
