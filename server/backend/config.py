from datetime import timedelta

SECRET_KEY = b''  #随机的一个密钥
SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = timedelta(days=31)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flask_demo"

MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
#此处删掉了邮箱名和密钥
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''

"""
"""
