from . import DBUtil

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
