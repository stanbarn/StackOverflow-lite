from passlib.hash import pbkdf2_sha256 as sha256

def question_to_json(single_question):
    json_result = {
        "questionId": single_question[0],
        "userId": single_question[1],
        "question": single_question[2],
        "createdOn": single_question[3],
        "userId": single_question[4],
        "username": single_question[5],
        "email": single_question[6],
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
        "userId": single_answer[3],
        "answer": single_answer[2],
        "createdOn": single_answer[4],
        "status": single_answer[5]
    }
    return json_result


def answers_to_json_list_utilities(answer_list):
    answers_list = []
    for item in answer_list:
        answers_list.append(answer_to_json(item))

    return answers_list


def generate_password_hash(password):
    return sha256.hash(password)


def verify_password_hash(password, hash):
    return sha256.verify(password, hash)

