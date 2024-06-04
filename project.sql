drop database if exists question_test;
create database question_test;
use question_test;

drop table if exists objective_questions;
create table objective_questions
(
    Objective_question_id int          not null comment '客观题编号'
        primary key,
    Description           varchar(255) not null comment '描述',
    ChoiceA               varchar(128) not null comment '选项A',
    ChoiceB               varchar(128) not null comment '选项B',
    ChoiceC               varchar(128) not null comment '选项C',
    ChoiceD               varchar(128) not null comment '选项D',
    Answer                char         not null comment '答案',
    Knowledge_points      varchar(18)  not null comment '知识点',
    Parse                 varchar(255) null comment '解析',
    Difficulty            float        not null comment '难度系数'
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
    userName varchar(18) not null comment '用户名'
        primary key,
    password varchar(18) not null comment '密码',
    roleId   int         not null comment '角色',
    constraint users_roles_roleId_fk
        foreign key (roleId) references roles (roleId)
)
    comment '用户表';

insert into roles (roleId, roleName) values (1, '管理员');
insert into roles (roleId, roleName) values (2, '教师');
insert into roles (roleId, roleName) values (3, '学生');

insert into users (userName, password, roleId) values ('test_user', 'py123', 3);
