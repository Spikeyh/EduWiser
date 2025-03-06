from flask import Blueprint, request, jsonify, session
from backend import db, SFid
from backend.models import User
from backend.encrypt import sha256
import requests
import json
import random
import string

# 定义蓝图
bp = Blueprint("login", __name__)


@bp.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.json
        types = data["type"]
        if types == "pwd":
            username = data["username"]
            pwd = data["password"]
            if pwd == "NULL":
                return jsonify({"code": 400, "msg": "error", "error": "username or password error"})
            try:
                user = User.query.filter_by(email=username).first()
                if user.getPassword() == sha256(pwd):
                    # session['username'] = user.username
                    session['uid'] = user.getUid()
                    return jsonify({"code": 200, "msg": "login", "login": "ok", "nickname": user.getNickname()})
                else:
                    return jsonify({"code": 400, "msg": "error", "error": "username or password error"})
            except Exception as e:
                print(e, flush=True)
                return jsonify({"code": 400, "msg": "error"})
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "error", "error": str(e)})


@bp.route("/api/login/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return jsonify({"code": 200, "msg": "logout", "logout": "ok"})


# 一键登录
# 登录并注册
@bp.route("/wx/login/auth", methods=["POST"])
def loginauth():
    try:
        data = request.json
        print(data)
        url_token = ""  #此处删掉了一个地址
        res = requests.get(url_token)
        print(res.text)
        token = res.json()["access_token"]
        url_phone = f""  #此处删掉了一个地址
        print(url_phone)
        data1 = {"code": data["code"]}
        data1 = json.dumps(data1)
        print(data1)
        res = requests.post(url_phone, data=data1)
        print(res.text)
        data = res.json()
        if data["errcode"] == 0:
            phonenumber = data["phone_info"]["phoneNumber"]
        else:
            return jsonify({"code": 400, "msg": "error", "error": "phonenumber error"})
        user = User.query.filter_by(phonenumber=phonenumber).first()
        if user is None:
            uid = SFid.get_id()
            nickname = "user_" + "".join(
                random.sample(string.ascii_letters + string.digits, 16)
            )
            new_user = User(
                uid=uid,
                nickname=nickname,
                password="NULL",
                email="NULL",
                phonenumber=phonenumber,
            )
            db.session.add(new_user)
            db.session.commit()
            session.clear()
            session["uid"] = uid
            user = new_user
        else:
            # session["username"] = user_info.user_name
            session["uid"] = user.getUid()
        return jsonify(
            {"code": 200, "msg": "login", "login": "ok", "nickname": user.getNickname()}
        )
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "error", "error": str(e)})


@bp.route("/api/test", methods=["GET", "POST"])
def test():
    uid = SFid.get_id()
    new_user = User(
        uid=uid,
        nickname="test",
        password=sha256("password"),
        email="NULL",
        phonenumber="NULL"
    )
    db.session.add(new_user)
    db.session.commit()

    # 清空 session
    session.clear()
    session["uid"] = uid
    # session["username"] = user_name
    user = new_user
    print(user.getPassword(), flush=True)
    return jsonify({"code": 200, "msg": "test", "test": "ok", "nickname": user.getNickname()})


@bp.route("/api/user", methods=["GET", "POST"])
def testuser():
    uid = session["uid"]
    user = User.query.filter_by(uid=uid).first()
    print(user.getPassword(), flush=True)
    return jsonify({"code": 200, "msg": "test", "test": "ok", "nickname": user.getNickname()})
