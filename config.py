class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    debug = True
    DEBUG=None
    SQLALCHEMY_DATABASE_URI = "sqlite:///pulpo.db"
