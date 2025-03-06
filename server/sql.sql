create database flask_demo;
use flask_demo;
create table user(
    user_id BIGINT primary key,
    user_name varchar(32) not null,
    user_password varchar(64) not null,
    email_address varchar(32) not null unique
);

CREATE TABLE input_info (
    info_id BIGINT PRIMARY KEY,
    info_time DATETIME NOT NULL,
    user_id BIGINT, 
    mother_profession VARCHAR(32) NOT NULL, -- 母亲职业
    father_profession VARCHAR(32) NOT NULL, -- 父亲职业
    mother_education VARCHAR(32) NOT NULL, -- 母亲教育程度
    father_education VARCHAR(32) NOT NULL, -- 父亲教育程度
    sibling_variables VARCHAR(32) NOT NULL, -- 同胞变量
    gender VARCHAR(32) NOT NULL, -- 性别
    ethnicity VARCHAR(32) NOT NULL, -- 民族
    household_registration VARCHAR(32) NOT NULL, -- 户籍
    date_of_birth VARCHAR(32) NOT NULL, -- 出生日期
    province VARCHAR(32) NOT NULL, -- 省份
    FOREIGN KEY (user_id) REFERENCES user(user_id) -- 外键定义
);

CREATE TABLE output_info (
    output_id BIGINT PRIMARY KEY,
    info_id BIGINT,
    user_id BIGINT, 
    output_time DATETIME NOT NULL,
    mother_profession SMALLINT,
    father_profession SMALLINT,
    mother_education SMALLINT,
    father_education SMALLINT,
    sibling_variables SMALLINT,
    gender SMALLINT,
    ethnicity SMALLINT,
    household_registration SMALLINT,
    date_of_birth SMALLINT,
    province VARCHAR(32),
    output_result VARCHAR(1024) NOT NULL,
    FOREIGN KEY (info_id) REFERENCES input_info(info_id) -- 定义外键，引用 input_info 表
    FOREIGN KEY (user_id) REFERENCES user(user_id) -- 外键定义
);
