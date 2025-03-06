from backend import db


class User(db.Model):
    uid = db.Column(db.BigInteger, primary_key=True)
    nickname = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(32))
    phonenumber = db.Column(db.String(13))

    def getUid(self):
        return self.uid

    def getNickname(self):
        return self.nickname

    def getEmail(self):
        return self.email

    def getPhonenumber(self):
        return self.phonenumber

    def getPassword(self):
        return self.password


class Input_info(db.Model):
    info_id = db.Column(db.BigInteger, primary_key=True)
    info_time = db.Column(db.DateTime, nullable=False)
    uid = db.Column(db.BigInteger, db.ForeignKey("user.uid"))
    mother_profession = db.Column(db.String(32), nullable=False)
    father_profession = db.Column(db.String(32), nullable=False)
    mother_education = db.Column(db.String(32), nullable=False)
    father_education = db.Column(db.String(32), nullable=False)
    sibling_variables = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.String(32), nullable=False)
    ethnicity = db.Column(db.String(32), nullable=False)
    household_registration = db.Column(db.String(32), nullable=False)
    date_of_birth = db.Column(db.String(32), nullable=False)
    province = db.Column(db.String(32), nullable=False)

    def to_dict(self):
        return {
            "info_id": self.info_id,
            "info_time": self.info_time,
            "mother_profession": self.mother_profession,
            "father_profession": self.father_profession,
            "mother_education": self.mother_education,
            "father_education": self.father_education,
            "sibling_variables": self.sibling_variables,
            "gender": self.gender,
            "ethnicity": self.ethnicity,
            "household_registration": self.household_registration,
            "date_of_birth": self.date_of_birth,
            "province": self.province
        }


class Output_info(db.Model):
    output_id = db.Column(db.BigInteger, primary_key=True)
    info_id = db.Column(db.BigInteger, db.ForeignKey("input_info.info_id"))
    uid = db.Column(db.BigInteger, db.ForeignKey("user.uid"))
    output_time = db.Column(db.DateTime, nullable=False)
    mother_profession = db.Column(db.SmallInteger)
    father_profession = db.Column(db.SmallInteger)
    mother_education = db.Column(db.SmallInteger)
    father_education = db.Column(db.SmallInteger)
    sibling_variables = db.Column(db.SmallInteger)
    gender = db.Column(db.SmallInteger)
    ethnicity = db.Column(db.SmallInteger)
    household_registration = db.Column(db.SmallInteger)
    date_of_birth = db.Column(db.SmallInteger)
    province = db.Column(db.String(32))
    output_result = db.Column(db.String(1024), nullable=False)

    def to_dict(self):
        return {
            "info_id": self.info_id,
            "output_time": self.output_time,
            "output_result": self.output_result
        }
