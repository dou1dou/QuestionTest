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


drop table if exists users;
create table users
(
    userName        varchar(18)   not null comment '用户名'
        primary key,
    password        varchar(18)   not null comment '密码',
    roleId          int           not null comment '角色',
    lastLoginCookie varchar(32)   null comment '上次登录的cookie',
    classroom       varchar(32)   null comment '教学班名称',
    real_name       varchar(16)   null comment '实名信息',
    deleted         int default 0 not null comment '是否申请注销，申请注销为1，否则为0',
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
        foreign key (username) references users (userName) on delete cascade
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

drop table if exists homework;
create table homework
(
    homework_id  int auto_increment comment '作业编号'
        primary key,
    question_id  int         not null comment '作业对应的问题编号',
    publisher    varchar(32) null comment '发布人',
    classroom_id int         null,
    publish_time datetime    not null comment '作业发布时间',
    cutoff_time  datetime    not null comment '作业截止时间',
    constraint homework_classroom_class_id_fk
        foreign key (classroom_id) references classroom (class_id),
    constraint homework_objective_questions_Objective_question_id_fk
        foreign key (question_id) references objective_questions (Objective_question_id),
    constraint homework_users_userName_fk
        foreign key (publisher) references users (userName)
            on update cascade on delete set null
)
    comment '作业表';

drop table if exists discussion;
create table discussion
(
    discussion_id int auto_increment comment '讨论信息编号'
        primary key,
    publisher     varchar(32)   not null comment '发布人',
    class_id      int           not null comment '消息所属教学班编号',
    content       varchar(1024) not null comment '讨论内容',
    constraint discussion_classroom_class_id_fk
        foreign key (class_id) references classroom (class_id),
    constraint discussion_users_userName_fk
        foreign key (publisher) references users (userName)
            on update cascade on delete cascade
)
    comment '讨论信息表';

drop table if exists student_homework;
create table student_homework
(
    stu_name    varchar(32)   not null comment '学生姓名',
    homework_id int           not null comment '作业编号',
    finished    int default 0 not null comment '是否完成，完成为1，否则为0',
    constraint student_homework_homework_homework_id_fk
        foreign key (homework_id) references homework (homework_id),
    constraint student_homework_users_userName_fk
        foreign key (stu_name) references users (userName)
)
    comment '学生信息和作业联合查询表';

drop trigger if exists sync_update_student_homework;
create trigger sync_update_student_homework after insert on homework for each row
    begin
        set @classroom = new.classroom_id;
        set @homework_id = new.homework_id;
        insert into student_homework (stu_name, homework_id)
            select users.userName, @homework_id from users where classroom = @classroom;
    end;

drop table if exists exam;
create table exam
(
    exam_id      int comment '考试编号' auto_increment
        primary key,
    exam_name    varchar(32)     not null comment '考试名称',
    publisher    varchar(32)     null comment '考试发布人',
    exam_time    int default 100 not null comment '考试时间（单位：分钟）',
    start_time   datetime        not null comment '考试开始时间',
    end_time     datetime        not null comment '考试截止时间',
    classroom_id int             null comment '所属班级',
    constraint exam_classroom_class_id_fk
        foreign key (classroom_id) references classroom (class_id),
    constraint exam_users_userName_fk
        foreign key (publisher) references users (userName)
)
    comment '考试信息表';

drop table if exists question_exam;
create table question_exam
(
    question_id int null comment '考试题目编号',
    exam_id     int null comment '对应考试编号',
    constraint question_exam_exam_exam_id_fk
        foreign key (exam_id) references exam (exam_id),
    constraint question_exam_objective_questions_Objective_question_id_fk
        foreign key (question_id) references objective_questions (Objective_question_id)
)
    comment '考试题目表';

create index question_exam_exam_id_index
    on question_exam (exam_id)
    comment '根据考试编号建立的索引';


insert into roles (roleId, roleName) values (1, '管理员');
insert into roles (roleId, roleName) values (2, '教师');
insert into roles (roleId, roleName) values (3, '学生');

insert into users (userName, password, roleId) values ('test_user', 'py123', 3);
insert into users (userName, password, roleId) values ('admin01', 'admin01', 1);
insert into users (userName, password, roleId) values ('teacher01', 'teacher01', 2);
insert into users (userName, password, roleId) values ('student01', 'student01', 3);
insert into users (userName, password, roleId) values ('student02', 'student02', 3);
insert into users (userName, password, roleId) values ('student03', 'student03', 3);

insert into course (course_name) values ('Python');
insert into course (course_name) values ('C');
insert into course (course_name) values ('Java');

insert into classroom (course_id, class_name, teacher_username) values (1, 'python实践教学', 'teacher01');
insert into classroom (course_id, class_name, teacher_username) values (1, 'python实践教学2', 'teacher01');
insert into classroom (course_id, class_name, teacher_username) values (1, 'python实践教学3', 'teacher01');

update users set classroom = 1 where userName = 'student01';
update users set classroom = 1 where userName = 'student02';
update users set classroom = 2 where userName = 'student03';

