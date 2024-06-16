import random

from django.http import JsonResponse
from django.shortcuts import render

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
            cursor.execute('select * from users where userName = %s and password = %s', (username, password))
            if len(cursor.fetchall()) != 0:
                # 登陆成功的逻辑操作
                response = JsonResponse({'login': True})
                if cookie is None:
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
        cursor.execute('select * from users where userName = %s', (username,))
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
    return register_api(username, password, 3)


def register_api_teacher(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    return register_api(username, password, 2)


def register_api_admin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    return register_api(username, password, 1)


def register(request):
    return render(request, 'register.html')


def question_get_api(request):
    if request.method == 'POST':
        return JsonResponse({'err': 'Please try with GET method! '})
    limit = request.GET.get('limit')
    difficulty = request.GET.get('difficulty', None)
    point = request.GET.get('knowledge_point', None)
    _questions = QuestionUtil.get_all_questions()
    target_questions = [q for q in _questions if _questions[-1] == difficulty] \
        if difficulty is not None else _questions
    target_questions = [q for q in target_questions if _questions[-3] == point] \
        if point is not None else target_questions
    if len(target_questions) < limit:
        response = {}
        for i in range(len(target_questions)):
            response[i] = ';'.join(target_questions[i][1:6])
            return JsonResponse(response)
    response = {}
    for i in range(limit):
        choice = random.randint(0, len(target_questions) - 1)
        response[i] = ';'.join(target_questions[choice][1:6])
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
        cursor.execute('select * from users where userName = %s', (username,))
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


def homepage_info_api(request):
    cookie = request.COOKIES.get('login')
    if cookie is None:
        return JsonResponse({'hasLogin': False})
    user_info = {}
    connection = None
    cursor = None
    try:
        connection = DBUtil.get_connection('user_pool')
        cursor = connection.cursor()
        cursor.execute('select * from users where lastLoginCookie = %s', (cookie,))
        res = cursor.fetchall()
        if len(res) == 0:
            return JsonResponse({'hasLogin': False})
        res = res[0]
        user_info['user_name'] = res[0]
        user_info['user_password'] = res[1]
        user_info['user_role_id'] = res[2]
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
