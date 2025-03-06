from flask import Blueprint, request, jsonify, session
from flask_mail import Message
from backend import db, mail, SFid
from backend.models import User
from backend.encrypt import sha256
import re
import time
import random


# 生成随机验证码
def generate_verification_code(length=6):
    return "".join(random.choices("0123456789", k=length))


# 发送验证码邮件
def send_verification_email(email, code):
    msg = Message("验证码", recipients=[email])
    msg.body = f"你的验证码是{code}。验证码有效期为5分钟，请尽快使用。"
    mail.send(msg)


# 校验邮箱格式
def is_valid_email(email):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None


# 校验验证码是否有效
def is_code_valid(sent_time, max_age=300):
    return time.time() - sent_time <= max_age


# 封装检查用户是否存在的逻辑
def get_user_by_email(email):
    return User.query.filter_by(email_address=email).first()


# 定义蓝图
bp = Blueprint("register", __name__)


@bp.route("/api/register/send_code", methods=["POST"])
def send_code():
    try:
        data = request.json
        email = data.get("email")

        if not email or not is_valid_email(email):
            return jsonify({"code": 400, "msg": "error", "error": "invalid email"})
        
        if get_user_by_email(email):
            return jsonify({"code": 400, "msg": "error", "error": "email already exists"})

        # 生成验证码并发送邮件
        code = generate_verification_code()
        send_verification_email(email, code)

        # 将验证码和邮箱存入 session
        session["code"] = sha256(code)
        session["email"] = sha256(email)
        session["time"] = time.time()

        return jsonify({"code": 200, "msg": ""})
    
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "error", "error": str(e)})


@bp.route("/api/register/register", methods=["POST"])
def register():
    try:
        data = request.json
        nickname = data.get("nickname")
        password = data.get("password")
        input_email = data.get("email")
        input_code = data.get("code")
        stored_email = session.get("email")
        stored_code = session.get("code")

        if not input_email or not nickname or not password:
            return jsonify({"code": 400, "msg": "error", "error": "invalid input"})
        
        if sha256(input_email) != stored_email or sha256(input_code) != stored_code:
            return jsonify({"code": 400, "msg": "error", "error": "invalid code"})

        if is_code_valid(session["time"]):
            return jsonify({"code": 400, "msg": "error", "error": "invalid code"})
        
        # 创建用户
        uid = SFid.get_id()
        new_user = User(
            uid=uid,
            nickname=nickname,
            password=sha256(password),
            email=input_email,
            phonenumber="NULL"
        )
        db.session.add(new_user)
        db.session.commit()

        # 清空 session
        session.clear()
        session["uid"] = uid
        # session["username"] = user_name

        return jsonify({"code": 200, "msg": "register", "register": "ok", "username": nickname})
    
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "error", "error": str(e)})


# @bp.route("/api/register/change_username", methods=["POST"])
# def change_username():
#     try:
#         uid = session.get("uid")
#         if not uid:
#             return jsonify({"code": 400, "msg": "登录已过期"})

#         data = request.json
#         username = data.get("username")

#         user = User.query.filter_by(user_id=uid).first()
#         if user:
#             user.user_name = username
#             db.session.commit()
#             return jsonify({"code": 200, "msg": "修改成功"})
#         return jsonify({"code": 400, "msg": "用户不存在"})
    
#     except Exception as e:
#         print(e, flush=True)
#         return jsonify({"code": 400, "msg": "错误", "error": str(e)})


# # 新增修改密码逻辑
# @bp.route("/api/register/change_password", methods=["POST"])
# def change_password():
#     try:
#         uid = session.get("uid")
#         if not uid:
#             return jsonify({"code": 400, "msg": "登录已过期"})

#         data = request.json
#         old_password = data.get("old_password")
#         new_password = data.get("new_password")

#         if not old_password or not new_password:
#             return jsonify({"code": 400, "msg": "缺少必要的字段"})

#         user = User.query.filter_by(user_id=uid).first()
#         if user and sha256(old_password) == user.user_password:
#             user.user_password = sha256(new_password)
#             db.session.commit()
#             return jsonify({"code": 200, "msg": "密码修改成功"})
#         return jsonify({"code": 400, "msg": "旧密码错误"})

#     except Exception as e:
#         print(e, flush=True)
#         return jsonify({"code": 400, "msg": "错误", "error": str(e)})
