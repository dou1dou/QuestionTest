insert into homework (question_id, publisher, classroom_id, publish_time, cutoff_time) values (1, 'teacher01', 1, '2024-06-18 17:17:11', '2024-06-24 17:17:11');

insert into exam (exam_id, exam_name, publisher, exam_time, start_time, end_time, classroom_id) values (1, 'Python实践教学', 'teacher01', 120, '2024-06-18 17:17:11', '2024-06-18 17:17:11', 1)
insert into question_exam (question_id, exam_id) values
                                                     (1, 1),
                                                     (2, 1),
                                                     (3, 1),
                                                     (4, 1)

