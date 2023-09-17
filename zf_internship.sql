use zf_internship;

create table state (
    state_id int auto_increment primary key ,
    mbjd varchar(10) not null comment '移动端经度',
    mbwd varchar(10) not null comment '移动端维度',
    yxwc int default 500,
    kqjd float8 not null comment '经度',
    kqwd float8 not null comment '维度',
    kqddxx varchar(100) not null comment '考勤地址',
    rwxm_id varchar(32) not null default 'FEFEA3511E0E2A53E0533E02CD0A5C05' comment 'id',
    kqlx int default 0 not null ,
    zkqfw int default 1 comment '是否在考勤范围'
 );

create table user(
    user_id int auto_increment primary key,
    ZFTAL_CSRF_TOKEN varchar(64) not null comment '正方用户Token',
    yhm int(10) not null comment '用户名',
    mm varchar(100) not null comment '密码',
    mail varchar(50) not null comment '邮箱'
);