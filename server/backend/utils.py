from backend.models import Input_info, Output_info
import time
from datetime import datetime
# 在此处量化数据
# 并返回原始数据对象，和量化数据对象
def quantitative_data(data, user_id, info_id, output_id):
    info_time = datetime.now()
    mother_profession = data['mother_profession']
    father_profession = data['father_profession']
    mother_education = data['mother_education']
    father_education = data['father_education']
    sibling_variables = data['sibling_variables']
    gender = data['gender']
    ethnicity = data['ethnicity']
    household_registration = data['household_registration']
    date_of_birth = data['date_of_birth']
    province = data['province']
    new_info = Input_info(info_id=info_id, info_time=info_time, user_id=user_id, mother_profession=mother_profession,
                            father_profession=father_profession, mother_education=mother_education,
                            father_education=father_education, sibling_variables=sibling_variables, gender=gender,
                            ethnicity=ethnicity,household_registration=household_registration,date_of_birth=date_of_birth,
                            province=province
    )
    """
    在此处量化输入，暂时省略
    """
    new_output = Output_info(output_id = output_id, info_id=info_id, output_time=datetime.now(), user_id=user_id,
                             mother_profession=1, father_profession = 1,
                             mother_education=1, father_education=1, 
                             sibling_variables=1, gender=1, ethnicity=1,
                             household_registration=1, date_of_birth=1, province="测试",
                             output_result="")
    return new_info, new_output

def analytical_results(output):
    output.output_time = datetime.now()
    output.output_result = "测试输出"
    return output
# info_id
# ,info_time
# ,user_id
# ,mother_profession
# ,father_profession
# ,mother_education
# ,father_education
# ,sibling_variables
# ,gender
# ,ethnicity
# ,household_registration
# ,date_of_birth
# ,province