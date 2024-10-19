from flask import Blueprint, request, jsonify, session
# from backend import Session,db
from backend.models import User
from backend.encrypt import hash
# 定义蓝图
bp = Blueprint("login", __name__)


@bp.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.json
        type = data["type"]
        if type == "pwd":
            user = data["user"]
            pwd = data["pwd"]
            try:
                user_info = User.query.filter_by(email_address=user).first()
                if user_info.user_password == hash(pwd):
                    session['username'] = user_info.user_name
                    session['uid'] = user_info.user_id
                    return jsonify({"code": 200, "msg": "登录成功", "username": user_info.user_name})
                else:
                    return jsonify({"code": 400, "msg": "账号或密码错误"})
            except Exception as e:
                print(e, flush=True)
                return jsonify({"code": 400, "msg": "账号或密码错误"})
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "错误", "error":str(e)})

@bp.route("/api/login/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return jsonify({"code": 200, "msg": "退出成功"})