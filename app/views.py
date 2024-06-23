import random

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ._utils import DBUtil, QuestionUtil


# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def login_api(request):
    # 负责登陆验证的api
    connection = None
    cursor = None
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            cookie = request.COOKIES.get('login', None)
            if username is None or password is None:
                return JsonResponse({'err': 'information is null'})
            connection = DBUtil.get_connection('user_pool')
            cursor = connection.cursor()
            cursor.execute('select * from users where userName = %s and password = %s and deleted = 0',
                           (username, password))
            if len(cursor.fetchall()) != 0:
                # 登陆成功的逻辑操作
                response = JsonResponse({'login': True})
                response.set_cookie('login', username + password, max_age=86400 * 7)
                cursor.execute("update users set lastLoginCookie = %s where userName = %s",
                               (username + password, username))
                connection.commit()
                return response
            else:
                return JsonResponse({'login': False})
        else:
            return JsonResponse({'login': False})
    except Exception as e:
        print(e)
        return JsonResponse({'login': 'db err!'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def register_api(username, password, role_id):
    print(username, password, role_id)
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('user_pool')
        cursor = connection.cursor()
        cursor.execute('select * from users where userName = %s and deleted = 0', (username,))
        if len(cursor.fetchall()) != 0:
            return JsonResponse({'err': 'user name already exists'})
        cursor.execute('insert into users (userName, password, roleId) values (%s, %s, %s)',
                       (username, password, role_id))
        connection.commit()
        return JsonResponse({'register': 'successful'})
    except Exception as e:
        print(e)
        return JsonResponse({'register': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def register_api_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    role_id = int(request.POST.get('role-id', 3))
    if role_id != 2 and role_id != 3:
        role_id = 3
    return register_api(username, password, role_id)


def register(request):
    return render(request, 'register.html')


def question_get_api(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'Please try with GET method! '})
    limit = int(request.GET.get('limit', 20))  # 将 limit 转换为整数
    difficulty = int(request.GET.get('Difficulty', -1))
    point = request.GET.get('Knowledge_points', None)
    if point == 'null' or len(point) == 0:
        point = None
    _questions = QuestionUtil.get_all_questions()

    # 使用列表推导式简化筛选逻辑
    target_questions = [q for q in _questions if
                        (difficulty is None or q[-1] == difficulty) and (point is None or q[-3] == point)]

    # 检查 target_questions 是否为空或 limit 是否过大
    if len(target_questions) == 0:
        return JsonResponse({'error': '没有找到符合条件的题目'})

    actual_limit = min(limit, len(target_questions))  # 确保 limit 不超过题目数量

    response = {}
    for i in range(actual_limit):
        choice = random.randint(0, len(target_questions) - 1)
        response[i] = target_questions[choice][0:10]
        target_questions.pop(choice)
    return JsonResponse(response)


def forget_password_api(request):
    if request.method == 'GET':
        return JsonResponse({'err': 'Please try with POST method!'})
    connection = None
    cursor = None
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username is None or password is None:
        return JsonResponse({'err': 'Please enter username'})
    try:
        connection = DBUtil.get_connection('user_pool')
        cursor = connection.cursor()
        cursor.execute('select * from users where userName = %s and deleted = 0', (username,))
        if len(cursor.fetchall()) != 0:
            cursor.execute("update users set password = %s where userName = %s", (password, username))
            connection.commit()
            return JsonResponse({"reset": "successful"})
    except Exception as e:
        print(e)
        return JsonResponse({"reset": "failed"})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def forget_password(request):
    return render(request, 'forget_password.html')


def question_post_api(request):
    if request.method == 'GET':
        return JsonResponse({'err': 'Please try with POST method!'})
    description = request.POST.get('description')
    choice_a = request.POST.get('choice_a')
    choice_b = request.POST.get('choice_b')
    choice_c = request.POST.get('choice_c')
    choice_d = request.POST.get('choice_d')
    answer = request.POST.get('answer')
    knowledge_point = request.POST.get('knowledge_point')
    parse = request.POST.get('parse', '略')
    difficulty = request.POST.get('difficulty')
    if (description is None or
            choice_a is None or
            choice_b is None or
            answer is None or
            knowledge_point is None or
            parse is None or
            difficulty is None):
        return JsonResponse({'err': 'key info is missing'})
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('question_pool')
        cursor = connection.cursor()
        cursor.execute("select max(Objective_question_id) from objective_questions")
        max_id = cursor.fetchall()[0][0]
        cursor.execute("insert into objective_questions "
                       "(Objective_question_id, Description, ChoiceA, ChoiceB, ChoiceC, ChoiceD, "
                       "Answer, Knowledge_points, Parse, Difficulty) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (max_id + 1, description, choice_a, choice_b, choice_c, choice_d, answer,
                        knowledge_point, parse, difficulty))
        connection.commit()
        return JsonResponse({'insert': 'successful'})
    except Exception as e:
        print(e)
        return JsonResponse({'insert': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def question_post(request):
    return render(request, 'post_question.html')


def homepage(request):
    return render(request, 'homepage.html')


def get_personal_info(request):
    cookie = request.COOKIES.get('login')
    if cookie is None:
        return JsonResponse({'hasLogin': False})
    user_info = {}
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('user_pool')
        cursor = connection.cursor()
        cursor.execute('select * from users where lastLoginCookie = %s and deleted = 0', (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        res = res[0]
        user_info['user_name'] = res[0]
        user_info['user_password'] = res[1]
        user_info['user_role_id'] = '学生' if res[2] == 3 else '老师' if res[2] == 2 else '管理员'
        user_info['hasLogin'] = True
        return JsonResponse(user_info)
    except Exception as e:
        print(e)
        return JsonResponse({'hasLogin': False})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def questions(request):
    return render(request, 'questions.html')


def recommend(request):
    return render(request, 'recommend.html')


def teaching_classes(request):
    return render(request, 'teaching_classes.html')


def register_teacher(request):
    return render(request, 'register_teacher.html')


def get_class_info(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'Please try with GET method!'})
    cookie = request.COOKIES.get('login')
    if cookie is None:
        return JsonResponse({'hasLogin': False})
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('user_pool')
        cursor = connection.cursor()
        cursor.execute('select * from users where lastLoginCookie = %s and deleted = 0', (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        user_name = res[0][0]
        cursor.execute("select classroom from users where userName = %s and deleted = 0", (user_name,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'info': 'no data'})
        response = {'info': []}
        for r in res:
            cursor.execute("select class_name, teacher_username from classroom where class_id = %s", (r[0],))
            cur = cursor.fetchall()
            response['info'].append({'class_name': cur[0][0], 'teacher_username': cur[0][1]})
        return JsonResponse({'info': res})
    except Exception as e:
        print(e)
        return JsonResponse({'info': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def get_practice_info(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'Please try with GET method!'})
    cookie = request.COOKIES.get('login')
    if cookie is None:
        return JsonResponse({'hasLogin': False})
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('question_pool')
        cursor = connection.cursor()
        cursor.execute('select * from users where lastLoginCookie = %s and deleted = 0', (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        username = res[0][0]
        cursor.execute('select * from practice_record where username = %s', (username,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'info': 'no data'})
        response = {'info': []}
        for record in res:
            cursor.execute("select * from objective_questions where Objective_question_id = %s", (record[1],))
            question_info = cursor.fetchall()[0]
            response['info'].append({
                'question_description': question_info[1],
                'question_choice_a': question_info[2],
                'question_choice_b': question_info[3],
                'question_choice_c': question_info[4],
                'question_choice_d': question_info[5],
                'answer': question_info[6],
                'knowledge_point': question_info[7],
                'choose': res[3],
                'pass': res[4],
            })
        return JsonResponse(response)
    except Exception as e:
        print(e)
        return JsonResponse({'info': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def get_solved_question_number(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'Please try with GET method!'})
    cookie = request.COOKIES.get('login')
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('question_pool')
        cursor = connection.cursor()
        cursor.execute("select userName from users where lastLoginCookie = %s and deleted = 0", (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        user_name = res[0][0]
        cursor.execute("select count(*) from practice_record where username = %s", (user_name,))
        res = cursor.fetchall()
        return JsonResponse({'all': len(QuestionUtil.get_all_questions()), 'solved': int(res[0][0])})
    except Exception as e:
        print(e)
        return JsonResponse({'info': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def get_solved_homework_number(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'please try with GET method!'})
    cookie = request.COOKIES.get('login')
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('question_pool')
        cursor = connection.cursor()
        cursor.execute("select classroom from users where lastLoginCookie = %s and deleted = 0", (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        classroom_id = res[0][0]
        cursor.execute("select count(*) from homework where classroom_id = %s", (classroom_id,))
        res = cursor.fetchall()
        return JsonResponse({'all': res[0][0], 'solved': int(res[0][0])})
    except Exception as e:
        print(e)
        return JsonResponse({'info': '查询失败'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


@csrf_exempt
def store_practice_info(request):
    if request.method == "GET":
        return JsonResponse({'err': 'please try with POST method!'})
    question_id = request.POST.get('question_id')
    correct = request.POST.get('correct')
    choices = request.POST.get('choices')
    cookie = request.COOKIES.get('login')

    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('question_pool')
        cursor = connection.cursor()
        cursor.execute("select userName from users where lastLoginCookie = %s and deleted = 0", (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        username = res[0][0]
        cursor.execute("insert into practice_record (question_id, username, choices, pass) values (%s, %s, %s, %s)",
                       (question_id, username, choices, correct))
        connection.commit()
        return JsonResponse({'info': 'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'info': 'err'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def personal(request):
    return render(request, 'personal.html')


def get_correct_rate(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'please try with GET method!'})
    cookie = request.COOKIES.get('login')
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('user_pool')
        cursor = connection.cursor()
        cursor.execute("select username from users where lastLoginCookie = %s and deleted = 0", (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        username = res[0][0]
        cursor.execute("select count(*) from practice_record where username = %s", (username,))
        total = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from practice_record where username = %s and pass = 0", (username,))
        correct = cursor.fetchall()[0][0]
        return JsonResponse({"total": total, "correct": correct})
    except Exception as e:
        print(e)
        return JsonResponse({'info': 'err'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def get_discussion_message(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'please try with GET method!'})
    cookie = request.COOKIES.get('login')
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('user_pool')
        cursor = connection.cursor()
        cursor.execute("select classroom from users where lastLoginCookie = %s and deleted = 0", (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        classroom_id = res[0][0]
        cursor.execute("select publisher, content from discussion where class_id = %s", (classroom_id,))
        res = cursor.fetchall()
        response = {'info': []}
        for r in res:
            response['info'].append({'publisher': r[0], 'content': r[1]})
        return JsonResponse(response)
    except Exception as e:
        print(e)
        return JsonResponse({'info': 'err'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def get_class_message(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'please try with GET method!'})
    cookie = request.COOKIES.get('login')
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('user_pool')
        cursor = connection.cursor()
        cursor.execute("select classroom from users where lastLoginCookie = %s and deleted = 0", (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        classroom_id = res[0][0]
        cursor.execute("select publisher, content from classroom_message where classroom_id = %s", (classroom_id,))
        res = cursor.fetchall()
        response = {'info': []}
        for r in res:
            response['info'].append({'publisher': r[0], 'content': r[1]})
        return JsonResponse(response)
    except Exception as e:
        print(e)
        return JsonResponse({'info': 'err'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def get_question_number_by_difficulty(request):
    if request.method == 'POST':
        return JsonResponse({'err': "please try with GET method!"})
    cookie = request.COOKIES.get("login")
    difficulty = request.GET.get("difficulty")
    connection = None
    cursor = None

    try:
        connection = DBUtil.get_connection("question_pool")
        cursor = connection.cursor()
        cursor.execute("select userName from users where lastLoginCookie = %s", (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        username = res[0][0]
        cursor.execute("select count(*) from practice_record where username = %s and question_id in "
                       "(select Objective_question_id from objective_questions where Difficulty = %s)",
                       (username, difficulty))
        solved = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from objective_questions where Difficulty = %s", (difficulty,))
        total = cursor.fetchall()[0][0]
        return JsonResponse({'total': total, 'solved': solved})
    except Exception as e:
        print(e)
        return JsonResponse({'err': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def teacher_classroom(request):
    return render(request, 'teaching_classes.html')


def student_classroom(request):
    return render(request, 'students_classes.html')


def get_mistakes(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'please try with GET method!'})
    cookie = request.COOKIES.get("login")
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection("question_pool")
        cursor = connection.cursor()
        cursor.execute("select userName from users where lastLoginCookie = %s", (cookie,))
        response = cursor.fetchall()
        cursor.execute("select question_id from practice_record where username = %s and pass = 1", (response[0][0],))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'noMistakes': 'no data'})

        question_ids = [row[0] for row in res]

        # 防止 question_ids 为空
        if not question_ids:
            return JsonResponse({'noQuestions': 'no matching questions'})

        # 建立查询语句获取符合条件的题目数据
        format_strings = ','.join(['%s'] * len(question_ids))
        cursor.execute(f"select * from objective_questions where Objective_question_id in ({format_strings})",
                       tuple(question_ids))
        questions = cursor.fetchall()

        # 构建响应数据
        response_data = {'questions': []}

        # 遍历问题列表，构建响应数据
        for question in questions:
            response_data['questions'].append([
                question[0],  # question_id
                question[1],  # description
                question[2],  # choice_a
                question[3],  # choice_b
                question[4],  # choice_c
                question[5],  # choice_d
                question[6],  # answer
                question[7],  # knowledge_point
                question[8],  # parse
                question[9],  # difficulty
            ])
        return JsonResponse(response_data)

    except Exception as e:
        print(e)
        return JsonResponse({'err': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


@csrf_exempt
def del_mistakes(request):
    if request.method == 'GET':
        return JsonResponse({'err': 'please try with GET method!'})
    question_id = request.POST.get("question_id")
    cookie = request.COOKIES.get("login")
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection("question_pool")
        cursor = connection.cursor()
        cursor.execute("select userName from users where lastLoginCookie = %s", (cookie,))
        response = cursor.fetchall()
        cursor.execute("delete from practice_record where username = %s and question_id = %s",
                       (response[0][0], question_id))
        connection.commit()
        return JsonResponse({'success': 'delete success'})
    except Exception as e:
        print(e)
        return JsonResponse({'err': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def get_exam_list(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'please try with GET method!'})
    cookie = request.COOKIES.get("login")
    connection = None
    cursor = None

    try:
        connection = DBUtil.get_connection("question_pool")
        cursor = connection.cursor()
        cursor.execute("select userName, classroom from users where lastLoginCookie = %s", (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        username = res[0][0]
        classroom_id = res[0][1]
        cursor.execute("SELECT exam_id, exam_name, exam_time FROM exam WHERE classroom_id = %s", (classroom_id,))
        response = {'data': []}
        exams = cursor.fetchall()
        for exam in exams:
            response['data'].append({'exam-id': exam[0], 'exam-name': exam[1], 'exam-time': exam[2]})
        return JsonResponse(response)
    except Exception as e:
        print(e)
        return JsonResponse({'err': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def get_exam_detail(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'please try with GET method!'})
    exam_id = request.GET.get("exam-id")
    connection = None
    cursor = None

    try:
        connection = DBUtil.get_connection("question_pool")
        cursor = connection.cursor()
        cursor.execute("select question_id from question_exam where exam_id = %s", (exam_id,))
        res = cursor.fetchall()
        question_list = []
        for exam in res:
            cursor.execute("select * from objective_questions where Objective_question_id = %s", (exam[0],))
            question = cursor.fetchall()[0][0:6]
            question_list.append(list(question))
        return JsonResponse({'data': question_list})
    except Exception as e:
        print(e)
        return JsonResponse({'err': 'failed'})
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def exam_page(request):
    return render(request, 'Random_combination_tests.html')
