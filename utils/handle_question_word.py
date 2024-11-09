import random
from typing import Any
from entity.user import User
from entity.set_question import SetQuestion


def generate_random(len_question, number_sets):
    len = len_question
    number_set_question = number_sets
    arr = list(range(len))
    questions_in_set = len//number_set_question
    count = 0
    list_tmp = []
    list_set_question = []
    while len > questions_in_set:
        x = random.randint(0, len-1)
        list_tmp.append(arr[x])
        arr.pop(x)
        len = len-1
        count = count+1
        if (count == questions_in_set):
            count = 0
            list_set_question.append(list_tmp)
            list_tmp = []
    list_set_question.append(arr)
    return list_set_question


def create_data_question_user(db: Any, user_name, len_questions, number_sets):
    user = (
        db.session.query(User)
        .filter(User.username == user_name)
        .first()
    )
    if user != None:
        user_id = user.id
        list_questions = generate_random(len_questions, number_sets)
        list_sets = []
        for i in range(len(list_questions)):
            data_list_question = "_".join(map(str, list_questions[i]))
            set_question = SetQuestion(
                name_set=(i+1), list_question=data_list_question, user_id=user_id)
            list_sets.append(set_question)
        db.session.add_all(list_sets)
        db.session.commit()
        return True
    else:
        return False
