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
    connection = None
    cursor = None
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username is None or password is None:
                return JsonResponse({'err': 'information is null'})
            connection = DBUtil.get_connection('user_pool')
            cursor = connection.cursor()
            cursor.execute('select * from users where userName = %s and password = %s', (username, password))
            return JsonResponse({'login': len(cursor.fetchall()) != 0})
        else:
            return JsonResponse({'login': False})
    except Exception as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()


def register_api(username, password, role_id):
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
    questions = QuestionUtil.get_all_questions()
    target_questions = [q for q in questions if questions[-1] == difficulty] if difficulty is not None else questions
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
