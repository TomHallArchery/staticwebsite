from website import db


class Run(db.Document):
    ''' Run ODM '''
    started = db.DateTimeField()


if __name__ == '__main__':
    pass
