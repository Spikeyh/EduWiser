from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# 模拟数据库
user_data = {}

# 上传用户输入的数据
@app.route('/api/post_info', methods=['POST'])
def post_info():
    data = request.json
    info_id = len(user_data) + 1  # 生成唯一的 info_id
    user_data[info_id] = data
    return jsonify({"code": 200, "msg": "数据上传成功", "info_id": info_id})

# 获取用户输入过的数据
@app.route('/api/get_info', methods=['GET', 'POST'])
def get_info():
    return jsonify({"code": 200, "count": len(user_data), "data": list(user_data.values()), "msg": "获取成功"})

# 修改用户上传过的某个案例数据
@app.route('/api/change_info', methods=['POST'])
def change_info():
    data = request.json
    info_id = data['info_id']
    if info_id in user_data:
        user_data[info_id] = data
        return jsonify({"code": 200, "msg": "数据修改成功"})
    return jsonify({"code": 400, "msg": "信息ID无效"}), 400

# 生成学历的逻辑
def generate_education(data):
    mother_education = data.get('mother_education')
    father_education = data.get('father_education')
    mother_profession = data.get('mother_profession')
    father_profession = data.get('father_profession')

    # 一个方案的示例
    if mother_education == '硕士' or father_education == '硕士':
        return "硕士"
    elif mother_profession in ['医生', '工程师'] or father_profession in ['医生', '工程师']:
        return "本科"
    elif mother_education == '大专' and father_education == '大专':
        return "专科"
    else:
        return random.choice(["高中", "初中"])  # 随机选择高中或初中

# 获取某个案例的输出结果
@app.route('/api/get_output', methods=['POST'])
def get_output():
    data = request.json
    info_id = data['info_id']
    if info_id in user_data:
        # 根据输入数据生成学历
        education_result = generate_education(user_data[info_id])
        output_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        return jsonify({
            "code": 200,
            "data": {
                "info_id": info_id,
                "education_result": education_result,
                "output_time": output_time
            },
            "msg": "获取成功"
        })
    return jsonify({"code": 400, "msg": "信息ID无效"}), 400

if __name__ == '__main__':
    app.run(debug=True)
