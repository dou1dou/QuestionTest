drop database if exists question_test;
create database question_test;
use question_test;

drop table if exists objective_questions;
create table objective_questions
(
    Objective_question_id int          not null comment '客观题编号'
        primary key,
    Description           varchar(255) null comment '描述',
    ChoiceA               varchar(128) null comment '选项A',
    ChoiceB               varchar(128)  null comment '选项B',
    ChoiceC               varchar(128)  null comment '选项C',
    ChoiceD               varchar(128) null comment '选项D',
    Answer                varchar(4)   null comment '答案',
    Knowledge_points      varchar(18)  null comment '知识点',
    Parse                 varchar(255) null comment '解析',
    Difficulty            int          null comment '难度系数'
)
    comment '试题表';


-- auto-generated definition
drop table if exists roles;
create table roles
(
    roleId   int         not null comment '角色编号'
        primary key,
    roleName varchar(12) not null comment '角色名称'
)
    comment '角色表';


-- auto-generated definition
drop table if exists users;
create table users
(
    userName        varchar(18) not null comment '用户名'
        primary key,
    password        varchar(18) not null comment '密码',
    roleId          int         not null comment '角色',
    lastLoginCookie varchar(32) null comment '上次登录的cookie',
    classroom       varchar(32) null comment '教学班名称',
    real_name       varchar(16) null comment '实名信息',
    constraint users_roles_roleId_fk
        foreign key (roleId) references roles (roleId)
)
    comment '用户表';

drop table if exists course;
create table course
(
    course_id   int auto_increment comment '课程编号',
    course_name varchar(32) not null comment '课程名称',
    constraint course_pk
        primary key (course_id),
    constraint course_pk_2
        unique (course_name)
)
    comment '课程信息表';

drop table if exists classroom;
create table classroom
(
    class_id         int auto_increment comment '教学班编号',
    course_id        int         null comment '课程编号',
    class_name       varchar(32) not null comment '教学班名称',
    teacher_username varchar(32) not null comment '教师用户名',
    constraint classroom_pk
        primary key (class_id),
    constraint classroom_course_course_id_fk
        foreign key (course_id) references course (course_id)
            on update cascade on delete set null,
    constraint classroom_users_userName_fk
        foreign key (teacher_username) references users (userName)
            on update cascade on delete cascade
);

drop table if exists practice_record;
create table practice_record
(
    record_id   int auto_increment comment '记录编号'
        primary key,
    question_id int           not null comment '题目编号',
    username    varchar(32)   not null comment '刷题用户名',
    choices     varchar(4)    not null comment '做题选项',
    pass        int default 0 not null comment '是否通过，通过为0，不通过为1',
    constraint practice_record_objective_questions_Objective_question_id_fk
        foreign key (question_id) references objective_questions (Objective_question_id),
    constraint practice_record_users_userName_fk
        foreign key (username) references users (userName)
)
    comment '刷题记录';

drop table if exists classroom_message;
create table classroom_message
(
    message_id   int auto_increment comment '信息编号'
        primary key,
    publisher    varchar(32)   not null comment '信息发布人',
    classroom_id int           not null comment '所属教学班编号',
    content      varchar(1024) not null comment '消息内容',
    constraint classroom_message_classroom_class_id_fk
        foreign key (classroom_id) references classroom (class_id),
    constraint classroom_message_users_userName_fk
        foreign key (publisher) references users (userName)
            on update cascade on delete cascade
)
    comment '教学班信息表';

drop table if exists classroom_message;
create table classroom_message
(
    message_id   int auto_increment comment '信息编号'
        primary key,
    publisher    varchar(32)   not null comment '信息发布人',
    classroom_id int           not null comment '所属教学班编号',
    content      varchar(1024) not null comment '消息内容',
    constraint classroom_message_classroom_class_id_fk
        foreign key (classroom_id) references classroom (class_id),
    constraint classroom_message_users_userName_fk
        foreign key (publisher) references users (userName)
            on update cascade on delete cascade
)
    comment '教学班信息表';




insert into roles (roleId, roleName) values (1, '管理员');
insert into roles (roleId, roleName) values (2, '教师');
insert into roles (roleId, roleName) values (3, '学生');

insert into users (userName, password, roleId) values ('test_user', 'py123', 3);

insert into course (course_name) values ('Python');
insert into course (course_name) values ('C');
insert into course (course_name) values ('Java');
