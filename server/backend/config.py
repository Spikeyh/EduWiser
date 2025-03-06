from datetime import timedelta

SECRET_KEY = b'n0}\x82X\x02Z\x15\xcf\x83\x08\x86\xe4\xb5\xf1\x92\xec\xaf\x17\xf1+ay\xf4'
SESSION_TYPE = "filesystem"
PERMANENT_SESSION_LIFETIME = timedelta(days=31)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flask_demo"

MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'neo_xyz_s@163.com'
MAIL_PASSWORD = 'JMnHdXvqYjyxZFhV'
MAIL_DEFAULT_SENDER = 'neo_xyz_s@163.com'
