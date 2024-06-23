import random
from _utils import DBUtil

try:
    first_set = set(random.sample(range(1, 881), 176))
    remaining_numbers = list(set(range(1, 881)) - first_set)
    second_set = set(random.sample(remaining_numbers, 264))
    remaining_numbers = list(set(range(1, 881)) - first_set - second_set)
    third_set = set(random.sample(remaining_numbers, 440))
    connection = DBUtil.get_connection("question_pool")
    cursor = connection.cursor()
    for number in first_set:
        cursor.execute("update objective_questions set difficulty = 3 where objective_question_id = %s", (number,))
    for number in second_set:
        cursor.execute("update objective_questions set difficulty = 2 where objective_question_id = %s", (number,))
    for number in third_set:
        cursor.execute("update objective_questions set difficulty = 1 where objective_question_id = %s", (number,))
    connection.commit()
except Exception as e:
    print(e)
finally:
    if connection is not None:
        connection.close()
    if cursor is not None:
        cursor.close()
