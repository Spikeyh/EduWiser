from flask import Flask, jsonify
from backend.snowflake import IdWorker
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
SFid = IdWorker(0, 0)
db = SQLAlchemy()
mail = Mail()
# app.json.ensure_ascii = False # 返回中文
@app.route("/")
def test():
    print(jsonify({"message": "你好世界"}), flush=True)
    return jsonify({"message": "你好世界"})
def create_app():
    app.config.from_object("backend.config")
    
    db.init_app(app)
    mail.init_app(app)
    Session(app)

    with app.app_context():
        from backend.login import bp as bp1
        app.register_blueprint(bp1)
        from backend.register import bp as bp2
        app.register_blueprint(bp2)
        from backend.info import bp as bp3
        app.register_blueprint(bp3)
        db.create_all()

    return app
