from flask import Blueprint, request, jsonify, session
from flask_mail import Message
from backend import db, mail, SFid
from backend.models import User
from backend.encrypt import hash
import re
import time
import random

"""
可以增加修改密码的逻辑
"""


# 生成随机验证码
def generate_verification_code(length=6):
    return "".join(random.choices("0123456789", k=length))


# 发送验证码邮件
def send_verification_email(email, code):
    msg = Message("验证码", recipients=[email])
    msg.body = f"你的验证码是{code}。验证码有效期为5分钟，请尽快使用。"
    mail.send(msg)


def is_valid_email(email):
    # 更严格的正则表达式
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None


# 定义蓝图
bp = Blueprint("register", __name__)

@bp.route("/api/register/send_code", methods=["POST"])
def send_code():
    try:
        # session.clear()
        data = request.json
        email = data["email"]
        print(email)
        if not is_valid_email(email):
            return jsonify({"code": 400, "msg": "邮箱格式不正确"})
        user = User.query.filter_by(email_address=email).first()
        if user:
            return jsonify({"code": 400, "msg": "邮箱已存在"})
        code = generate_verification_code()
        send_verification_email(email, code)
        session["code"] = hash(code)
        session["email"] = email
        session["time"] = time.time()
        return jsonify({"code": 200, "msg": "验证码已发送，请注意查收"})
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "错误", "error":str(e)})


@bp.route("/api/register/check_code", methods=["POST"])
def check_code():
    try:
        data = request.json
        code = data["code"]
        email = data["email"]
        email1 = session["email"]
        if email1 != email:
            return jsonify({"code": 400, "msg": "邮箱不正确"})
        code1 = session["code"]
        if hash(code) != code1:
            return jsonify({"code": 400, "msg": "验证码不正确"})
        code_sent_time = session["time"]
        if time.time() - code_sent_time > 300:
            return jsonify({"code": 400, "msg": "验证码已过期"})
        session.pop("code")
        session["time"] = time.time()
        return jsonify({"code": 200, "msg": "验证码正确"})

    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "错误", "error":str(e)})


@bp.route("/api/register/register", methods=["POST"])
def register():
    try:
        data = request.json
        user_name = data["username"]
        user_password = data["password"]
        user_password = hash(user_password)
        code_sent_time = session["time"]
        email = session["email"]
        if time.time() - code_sent_time > 600:
            return jsonify({"code": 400, "msg": "注册超时，请重新注册"})
        user_id = SFid.get_id()
        new_user = User(
            user_id=user_id,
            user_name=user_name,
            user_password=user_password,
            email_address=email,
        )
        db.session.add(new_user)
        db.session.commit()
        session.clear()
        session["uid"] = user_id
        session["username"] = user_name
        return jsonify({"code": 200, "msg": "注册成功"})
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "错误", "error":str(e)})





@bp.route("/api/register/change_username", methods=["POST"])
def change_username():
    try:
        try:
            uid = session["uid"]
        except Exception as e:
            print(e, flush=True)
            return jsonify({"code": 400, "msg": "登录已过期"})
        data = request.json
        username = data["username"]
        user = User.query.filter_by(user_id=uid).first()
        user.user_name = username
        db.session.commit()
        return jsonify({"code": 200, "msg": "修改成功"})
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "错误", "error":str(e)})
