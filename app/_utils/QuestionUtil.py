from . import DBUtil
from djangoProject.settings import BASE_DIR
import os

connection = None
cursor = None
questions = None
try:
    connection = DBUtil.get_connection("question_pool")
    cursor = connection.cursor()
    cursor.execute("select * from objective_questions")
    questions = cursor.fetchall()
except Exception as e:
    print(e)
finally:
    if connection is not None:
        connection.close()
    if cursor is not None:
        cursor.close()

if not os.path.exists(str(BASE_DIR) + "/static/files"):
    os.makedirs(str(BASE_DIR) + "/static/files")
with open(str(BASE_DIR) + "/static/files/questions.csv", "w", encoding="utf-8") as f:
    f.write("Objective_question_id,Description,ChoiceA,ChoiceB,ChoiceC,ChoiceD,Answer,"
            "Knowledge_points,Parse,Difficulty\n")
    for q in questions:
        for i in range(len(q)):
            f.write(str(q[i]))
            if i != len(q) - 1:
                f.write(",")
        f.write("\n")


def get_all_questions():
    return questions


def update_all_questions():
    global questions, connection, cursor
    try:
        connection = DBUtil.get_connection("question_pool")
        cursor = connection.cursor()
        cursor.execute("select * from objective_questions")
        questions = cursor.fetchall()
    except Exception as ex:
        print(ex)
    finally:
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()
