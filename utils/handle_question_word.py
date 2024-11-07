import random


def generate_random():
    len = 60
    number_set_question = 30
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

    print(list_set_question)


generate_random()
