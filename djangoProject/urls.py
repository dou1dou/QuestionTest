"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views
import app.admin
from app import ChartViews

urlpatterns = [
    path('', views.index),
    path('app/admin/', app.admin.admin.site.urls),
    path('login/', views.login),
    path('login/api/', views.login_api),
    path('register/api/user/', views.register_api_user),
    path('register/', views.register),
    path('register/teacher/', views.register_teacher),
    path('forgetpassword/api/', views.forget_password_api),
    path('forgetpassword/', views.forget_password),
    path('postquestion/api/', views.question_post_api),
    path('postquestion/', views.question_post),
    path('homepage/', views.homepage),
    path('questions/', views.questions),
    path('recommend/', views.recommend),
    path('teaching_classes/', views.teaching_classes),
    path('info/personal/api/', views.get_personal_info),
    path('info/class/api/', views.get_class_info),
    path('info/practice/api/', views.get_practice_info),
    path('personal/', views.personal),
    path('questions/api/', views.question_get_api),
    path('questions/store/api/', views.store_practice_info),
    path('info/personal/get_solved_question_number/api/', views.get_solved_question_number),
    path('message/class/api/', views.get_class_message),
    path('message/discussion/api', views.get_discussion_message),
    path('info/personal/get_correct_rate/api/', views.get_correct_rate),
    path('info/personal/get_solved_homework_number/api/', views.get_solved_homework_number),
    path('classroom/student/', views.student_classroom),
    path('classroom/teacher/', views.teacher_classroom),
    path('get_mistakes/api/', views.get_mistakes),
    path('delete_mistakes/api/', views.del_mistakes),
    path('exam/list/api/', views.get_exam_list),
    path('exam/question/api/', views.get_exam_detail),
    path('exam/', views.exam_page),
    path('teacher_homepage/', views.teacher_homepage),
    path('teacher_questions/', views.teacher_question),
    path('teacher_personal/', views.teacher_personal),
    path('post_question/', views.post_question),
    path('logout/api/', views.logout_api),
]
