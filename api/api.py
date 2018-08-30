from flask import Flask, request, jsonify
import uuid
from pprint import pprint
import json
from api import  utilities
from api.models import Answer, Question, User, questions, users, answers
from flask import Blueprint
import re
from api.database import DatabaseConnection
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required

database = DatabaseConnection()
# database.fetch_username('test')
mod = Blueprint('questions', __name__)
json_utility = utilities

@mod.route('/')
def landing():
    return 'StackOverflow-Lite Api'


@mod.route('/signup', methods=['POST'])
def registerUser():
    """
    Function to enables user to sign up on the platform. It checks if all the
    required data is added by the user and then validates the email and password. Returns user object in for successful registration.
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user_id = uuid.uuid4()

    # check if username exists
    if not username or username.isspace():
        return jsonify({
            'message': 'Sorry, enter your username!'
        }), 400

    # check if email exists
    if not email or email.isspace():
        return jsonify({
            'message': 'Sorry, enter your email!'
        }), 400
    # check if password exists
    if not password or password.isspace():
        return jsonify({
            'message': 'Sorry, you did not enter your password!'
        }), 400

    # validate email address
    # source: https://docs.python.org/2/howto/regex.html
    if not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", email):
        return jsonify({
            'message': 'Invalid email address!'
        }), 400

    # validate password. make sure the password is strong
    # source: https://docs.python.org/2/howto/regex.html
    low = re.search(r"[a-z]", password)
    up = re.search(r"[A-Z]", password)
    num = re.search(r"[0-9]", password)
    if not all((low, up, num)):
        return jsonify({
            'message': 'Passwords should include upper and lower cases, and numeric characters'
        }), 400

    # make sure password has a minimum length of 6 characters
    if len(password) < 6:
        return jsonify({
            'message': 'Passwords should be at least 6 characters long!'
        }), 400

    # check if username already exists
    if database.fetch_user_by_username(username):
        return jsonify({
            'message': 'Sorry, that username is registered to another user!'
        }), 400

    # check if email exists
    if database.fetch_user_by_email(email):
        return jsonify({
            'message': 'Sorry, that email is registered to another user!'
        }), 400

    # create user object
    user = User(user_id, username, email, password)

    # hashed_password = generate_password_hash(password)
    try:
        if database.create_user(user_id, username, email, password):
            users.append(user)
            return jsonify({
                'Username': user.username,
                'message': '{} has registered successfully'.format(username)
            }), 201
        else:
            return jsonify({
                'Username': user.username,
                'message': '{} was not created '.format(username)
            }), 400

    except Exception as e:
        return jsonify({
            'Username': user.username,
            'message': '{} was not created '.format(e)
        }), 400


@mod.route('/signin', methods=['POST'])
def signinUser():
    """
    Function enables user to login.
    Returns a success message and the logged in user object in case of successful login.
    """
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Check that username has been supplied
    if not username or username.isspace():
        return jsonify({
            'message': 'You did not enter your username!'
        }), 400

    # Check that password has been supplied
    if not password or password.isspace():
        return jsonify({
            'message': 'You did not enter your password!'
        }), 400

    # Fetch user by username
    if not database.fetch_username(username):
        return jsonify({
            'message': 'Sorry, wrong username!'
        }), 400

    # Fetch user by username and password
    if not database.fetch_user_by_username_password(username, password):
        return jsonify({
            'message': 'Sorry, user does not exist!'
        }), 400
    # Get user Id and generate authentication token
    user = database.fetch_username(username)
    access_token = create_access_token(user)
    return jsonify({
        'token': access_token,
        'message': '{} is logged in.'.format(username)
    }), 200


@mod.route('/questions/add', methods=['POST'])
def add_question():
    """
    Function enables user to create a question
    """
    data = request.get_json()

    details = data.get('question')
    user_id = data.get('user_id')

    if not details or details.isspace():
        return jsonify({
            "message": "Sorry, you didn't enter any question!"
        }), 400

    qn = Question(user_id, details)

    questionrequest = qn.add_question()

    if not questionrequest:
        return jsonify({
            "message": "Sorry, you didn't enter any question!"
        }), 400

    question = qn.fetch_question(questionrequest)

    print(question)

    questions.append(question)

    return jsonify({
        "question": question,
        "message": "Question added successfully!"
    }), 201


@mod.route('/questions/answer/<int:questionId>', methods=['POST'])
def add_answer(questionId):
    """
    Function enables user to add an answer to a question on the platform..
    """
    data = request.get_json()

    details = data.get('details')

    try:
        if not details or details.isspace():
            return jsonify({
                'message': 'Sorry, you did not enter any answer!'
            }), 400
        if len(questions) == 0:
            return jsonify({
                'message': 'Sorry, there are no questions yet!!'
            }), 400

        question = questions[questionId - 1]
        answer = Answer(questionId, details)
        answers.append(answer)

        return jsonify({
            'Question': question.__dict__,
            'Answer': answer.__dict__,
            'Message': 'Answer added succesfully!'
        }), 201
    except IndexError:
        return jsonify({
            'message': 'Question does not exist.'
        }), 400

@mod.route('/questions/answers/<int:questionId>', methods=['GET'])
def get_answers(questionId):
    """
    Function enables user to get answers to a question on the platform..
    """

    try:

        question = database.fetch_question_by_id(questionId)
        if not question:
            return jsonify({
                'message': 'Question does not exist.'
            }), 400

        answerResponse = database.fetch_answers_for_question(questionId)

        if len(answerResponse) == 0:
            return jsonify({
                'message': 'No answer was found.'
            }), 400

        answers.append(answerResponse)

        return jsonify({
            'Question': question.__dict__,
            'Answer': answers.__dict__,
            'Message': 'answers to question!'
        }), 201

    except IndexError:
        return jsonify({
            'message': 'Question does not exist.'
        }), 400


@mod.route('/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    """
    Function enables a user to fetch a single question from the platform
    using the questionId .
    """
    if not questionId or questionId < 1:
        return jsonify({
            'message': 'Sorry! questionId cannot be null.'
        }), 404

    try:
        question = database.fetch_question_by_id(questionId)
        if not question:
            return jsonify({
                'message': 'Sorry! questionId cannot be null.'
            }), 404
        json_question = json_utility.question_to_json(question)
        answers = database.fetch_answers_for_question(questionId)
        if not answers or len(answers) < 1:
            return jsonify({
                'Answers': [],
                'Question': json_question,
                'Message': 'Question fetched successfully! but no answers found for it'
            }), 200

        answers_json = json_utility.answers_to_json_list_utilities(answers)

        # ans = filter(lambda a: a['questionId'] == questionId, answers)
        return jsonify({
            'Answers': answers_json,
            'Question': json_question,
            'Message': 'Question fetched successfully!'
        }), 200
    except IndexError:
        return jsonify({
            'message': 'Question does not exist.'
        }), 404


@mod.route('/questions/all', methods=['GET'])
def get_questions():
    """
    Function enables a user to fetch all questions
    """
    questionsResponse = database.fetch_all_questions()
    if len(questionsResponse) == 0:
        return jsonify({
            'message': 'Sorry there are no questions yet!'
        }), 400

    qnjson = json_utility.questions_to_json_list_utilities(questionsResponse)

    return jsonify({
        'Questions': qnjson,
        'message': 'Questions fetched successfully!'
    }), 200


@mod.route('/questions/remove/<int:questionId>', methods=['DELETE'])
def delete_question(question_Id):
    try:
        if database.delete_question(question_Id):
                return jsonify({
                    'message': 'Question deleted!'
                }), 200

    except IndexError:
        return jsonify({
            'message': 'Question does not exist.'
        }), 400


@mod.route('/qustions/<string:userId>', methods=['GET'])
def get_questions_for_user(user_id):
    """
    Function enables a user to fetch all questions
    """
    questions = database.fetch_questions_for_user(user_id)
    if len(questions) == 0:
        return jsonify({
            'message': 'Sorry there are no questions yet!'
        }), 400

    return jsonify({
        'Questions': [question.__dict__ for question in questions],
        'message': 'Questions fetched successfully!'
    }), 200