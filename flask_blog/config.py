class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "testalexit@yandex.ru"
    MAIL_PASSWORD = "ohbybunrhqxhjpnj"
