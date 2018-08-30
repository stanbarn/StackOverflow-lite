def question_to_json(single_question):
    json_result = {
        "questionId": single_question[0],
        "userId": single_question[1],
        "question": single_question[2]
    }
    return json_result


def questions_to_json_list_utilities(question_list):
    questions_list = []
    for item in question_list:
        questions_list.append(question_to_json(item))

    return questions_list


def answer_to_json(single_answer):
    json_result = {
        "answerId": single_answer[0],
        "questionId": single_answer[1],
        "userId": single_answer[2],
        "answer": single_answer[3]
    }
    return json_result


def answers_to_json_list_utilities(answer_list):
    answers_list = []
    for item in answer_list:
        answers_list.append(question_to_json(item))

    return answers_list

