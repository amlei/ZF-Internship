use zf_internship;
-- 位置
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
-- 用户
create table user(
    user_id int auto_increment primary key,
    ZFTAL_CSRF_TOKEN varchar(64) not null comment '正方用户Token',
    yhm int(10) not null comment '用户名',
    mm varchar(100) not null comment '密码',
    mail varchar(50) not null comment '邮箱'
);
-- 周报
create table report(
    report_id int auto_increment primary key,
    zrzlx int default 1,
    ywlyb varchar(1) default null,
    id1 varchar(1) default null,
    sxwd int default 1,
    kcsxwd int default 1,
    zc_h_zj int not null default 12 comment '周次',
    yf_h_zj varchar(1) default null,
    sfbx int default 0,
    xh_id int(10) not null comment '学号',
    zjld varchar(57) not null ,
    ksrq date not null default '2023-09-01' comment '实习开始日期',
    jsrq date not null default '2024-05-31'comment '实习结束日期',
    sxxx varchar(14) comment '所属',
    xzc int default 12,
    zc int default 1 not null comment '考勤周次',
    autocomplete varchar(1) default null,
    rzqssj date not null default (CURRENT_DATE - 5),
    rzjssj date not null default (CURRENT_DATE),
    zrznr varchar(1500) not null comment '周报内容',
    ewzrznr varchar(1) default null,
    file1 varchar(1) default null,
    fjxx varchar(1) default null,
    ywbjkey varchar(2) not null default 'zj'
);