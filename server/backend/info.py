from flask import session,request,Blueprint,jsonify,current_app, copy_current_request_context
from backend import db,SFid
from backend.models import Input_info,Output_info,User
from backend.utils import quantitative_data, analytical_results
bp = Blueprint('info', __name__)
@bp.route('/api/get_info', methods=["GET", "POST"])
def get_info():
    try:
        try:
            uid = session['uid']
            user = User.query.filter_by(user_id=uid).first()
            if not user:
                session.clear()
                return jsonify({"code": 400, "msg": "登录已过期"})
        except Exception as e:
            print(e, flush=True)
            return jsonify({"code": 400, "msg": "登录已过期"})
        count = Input_info.query.filter_by(user_id=uid).count()
        infos = Input_info.query.filter_by(user_id=uid).order_by(Input_info.info_time.desc()).all()
        result = [info.to_dict() for info in infos]
        return jsonify({"code": 200, "count": count, "msg": "获取成功", "data": result})

    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "错误", "error":str(e)})

@bp.route('/api/get_output', methods=["POST"])
def get_output():
    try:
        try:
            uid = session['uid']
            user = User.query.filter_by(user_id=uid).first()
            if not user:
                session.clear()
                return jsonify({"code": 400, "msg": "登录已过期"})
        except Exception as e:
            print(e, flush=True)
            return jsonify({"code": 400, "msg": "登录已过期"})
        data = request.get_json()
        info_id = data["info_id"]
        infos = Output_info.query.filter_by(info_id=info_id, user_id=uid).order_by(Output_info.output_time.desc()).first()
        if infos:
            result = infos.to_dict()
            return jsonify({"code": 200, "msg": "获取成功", "data": result})
        else:
            return jsonify({"code": 400, "msg": "结果生成中"})

    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "错误", "error":str(e)})


# def get_result(new_output):
#     try:
#         # 手动创建应用程序上下文
#         with current_app.app_context():
#             result = analytical_results(new_output)
#             db.session.add(result)
#             db.session.commit()
#     except Exception as e:
#         print(e, flush=True)
#         print("插入新结果错误")

@bp.route('/api/post_info', methods=["POST"])
def post_info():
    try:
        try:
            uid = session['uid']
            user = User.query.filter_by(user_id=uid).first()
            if not user:
                session.clear()
                return jsonify({"code": 400, "msg": "登录已过期"})
        except Exception as e:
            print(e, flush=True)
            return jsonify({"code": 400, "msg": "登录已过期"})
        data = request.get_json()
        
        new_info, new_output = quantitative_data(data, uid, info_id=SFid.get_id(), output_id=SFid.get_id())
        
        db.session.add(new_info)
        db.session.commit()

        # 在新线程中运行
        # th = Thread(target=get_result, args=(new_output,))
        # th.start()
        result = analytical_results(new_output)
        db.session.add(result)
        db.session.commit()
        return jsonify({"code": 200, "msg": "提交成功"})
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "错误", "error":str(e)})



@bp.route('/api/change_info', methods=["POST"])
def change_info():
    try:
        try:
            uid = session['uid']
            user = User.query.filter_by(user_id=uid).first()
            if not user:
                session.clear()
                return jsonify({"code": 400, "msg": "登录已过期"})
        except Exception as e:
            print(e, flush=True)
            return jsonify({"code": 400, "msg": "登录已过期"})
        data = request.get_json()
        new_info, new_output = quantitative_data(data, uid, info_id=data['info_id'], output_id=SFid.get_id())
        old_info = Input_info.query.filter_by(info_id=data['info_id']).first()
        old_info.mother_profession = new_info.mother_profession
        old_info.father_profession = new_info.father_profession
        old_info.mother_education = new_info.mother_education
        old_info.father_education = new_info.father_education
        old_info.sibling_variables = new_info.sibling_variables
        old_info.gender = new_info.gender
        old_info.ethnicity = new_info.ethnicity
        old_info.household_registration = new_info.household_registration
        old_info.date_of_birth = new_info.date_of_birth
        old_info.province = new_info.province
        old_info.info_time = new_info.info_time
        db.session.commit()
        # th = Thread(target=get_result, args=(new_output,))
        # th.start()
        result = analytical_results(new_output)
        db.session.add(result)
        db.session.commit()
        return jsonify({"code": 200, "msg": "修改成功"})
    except Exception as e:
        print(e, flush=True)
        return jsonify({"code": 400, "msg": "错误", "error":str(e)})