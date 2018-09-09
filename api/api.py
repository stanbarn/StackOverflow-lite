from flask import Flask, request, jsonify
import uuid
from api import utilities
from flask import Blueprint
import re
from api.database import DatabaseConnection
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_cors import CORS
from api import app
database = DatabaseConnection()
mod = Blueprint('questions', __name__)
json_utility = utilities
CORS(app)


@mod.route('/')
def landing():
    return 'StackOverflow-Lite Api'


@mod.route('/signup', methods=['POST'])
def create_user():
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
            'Message': 'Sorry, enter your username!'
        }), 400

    # check if email exists
    if not email or email.isspace():
        return jsonify({
            'Message': 'Sorry, enter your email!'
        }), 400
    # check if password exists
    if not password or password.isspace():
        return jsonify({
            'Message': 'Sorry, you did not enter your password!'
        }), 400

    # validate email address
    # source: https://docs.python.org/2/howto/regex.html
    if not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", email):
        return jsonify({
            'Message': 'Invalid email address!'
        }), 400

    # validate password. make sure the password is strong enough
    low = re.search(r"[a-z]", password)
    up = re.search(r"[A-Z]", password)
    num = re.search(r"[0-9]", password)
    if not all((low, up, num)):
        return jsonify({
            'Message': 'Passwords should include upper, lower cases, and numeric characters'
        }), 400

    # make sure password has a minimum length of 6 characters
    if len(password) < 6:
        return jsonify({
            'Message': 'Passwords should be at least 6 characters long!'
        }), 400

    # check if username already exists
    if database.fetch_user_by_username(username):
        return jsonify({
            'Message': 'Sorry, that username is registered to another user!'
        }), 400

    # check if email exists
    if database.fetch_user_by_email(email):
        return jsonify({
            'Message': 'Sorry, that email is registered to another user!'
        }), 400

    # hash password
    hashed_password = json_utility.generate_password_hash(password)
    try:
        if database.create_user(user_id, username, email, hashed_password):
            return jsonify({
                'Username': username,
                'Message': '{} has registered successfully'.format(username)
            }), 201
        else:
            return jsonify({
                'Username': username,
                'Message': '{} was not created '.format(username)
            }), 400
            
    except Exception as e:
        return jsonify({
            'Username': username,
            'Message': '{} was not created '.format(e)
        }), 400


@mod.route('/signin', methods=['POST'])
def signin_user():
    """
    Function enables user to login. Returns a success Message and the logged in user object in case of successful login.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Check that username has been supplied
    if not username or username.isspace():
        return jsonify({
            'Message': 'You did not enter your username!'
        }), 400

    # Check that password has been supplied
    if not password or password.isspace():
        return jsonify({
            'Message': 'You did not enter your password!'
        }), 400

    # Fetch user by username
    user = database.fetch_user_by_username(username)
    if user is None:
        return jsonify({
            'Message': 'Sorry, Failed  authentication. Username does not exist!'
        }), 400
    # check password is true
    if json_utility.verify_password_hash(password, user[3]):

        # Get user Id and generate authentication token
        access_token = create_access_token(username)
        return jsonify({
            'Token': access_token,
            'Message': '{} is logged in.'.format(username)
        }), 200
    else:
        return jsonify({
            'Message': 'Sorry, Failed  authentication. check username and password!'
        }), 400


@mod.route('/questions', methods=['POST'])
def add_question():
    """
    Function enables user to create a question
    """
    data = request.get_json()
    details = data.get('question')
    user_id = data.get('userId')

    if not details or details.isspace():
        return jsonify({
            "Message": "Sorry, you didn't enter any question!"
        }), 400

    question_request = database.create_question(user_id, details)

    if not question_request:
        return jsonify({
            "Message": "Sorry, you didn't enter any question!"
        }), 400

    question = database.fetch_question_by_id(question_request)

    question_json = json_utility.question_to_json(question)

    return jsonify({
        "Question": question_json,
        "Message": "Question added successfully!"
    }), 201


@mod.route('/questions/<int:questionId>/answers', methods=['POST'])
def add_answer(questionId):
    """
    Function enables user to add an answer to a question on the platform..
    """
    data = request.get_json()
    userId = data.get('userId')
    details = data.get('answer')

    try:
        if not details or details.isspace():
            return jsonify({
                'Message': 'Sorry, you did not enter any answer!'
            }), 400

        question = database.fetch_question_by_id(questionId)
        if not question:
            return jsonify({
                'Message': 'Sorry, question does not exist!'
            }), 400

        addAnswer = database.insert_answer_for_question(userId, questionId, details)
        if not addAnswer:
            return jsonify({
                'Message': 'Sorry, there are no questions yet!!'
            }), 400

        answer = database.fetch_answers_by_id(addAnswer)
        if answer is None:
            return jsonify({
                'Message': 'Sorry, errors occurred!!'
            }), 400

        questionJson = json_utility.question_to_json(question)
        answerJson = json_utility.answer_to_json(answer)

        # answers.append(addAnswer)

        return jsonify({
            'Question': questionJson,
            'Answer': answerJson,
            'Message': 'Answer added succesfully!'
        }), 201

    except IndexError:
        return jsonify({
            'Message': 'Question does not exist.'
        }), 400


@mod.route('/questions/answers/<int:questionId>', methods=['GET'])
def get_answers(questionId):
    """
    Function enables user to get answers to a question.
    """

    try:

        question = database.fetch_question_by_id(questionId)
        if not question:
            return jsonify({
                'Message': 'Question does not exist.'
            }), 400

        answer_response = database.fetch_answers_for_question(questionId)

        if len(answer_response) == 0:
            return jsonify({
                'Message': 'No answer was found.'
            }), 400
        
        question_json = json_utility.question_to_json(question)
        answer_json = json_utility.answers_to_json_list_utilities(answer_response)

        return jsonify({
            'Question': question_json,
            'Answer': answer_json,
            'Message': 'answers to question!'
        }), 200

    except IndexError:
        return jsonify({
            'Message': 'Question does not exist.'
        }), 400


@mod.route('/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    """
    Function enables a user to fetch a single question from the platform
    using the questionId .
    """
    if not questionId or questionId < 1:
        return jsonify({
            'Message': 'Sorry! questionId cannot be null.'
        }), 404

    try:
        question = database.fetch_question_by_id(questionId)
        if not question:
            return jsonify({
                'Message': 'Sorry! questionId cannot be null.'
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
            'Message': 'Question does not exist.'
        }), 404


@mod.route('/questions', methods=['GET'])
def get_questions():
    """
    Function enables a user to fetch all questions
    """
    questionsResponse = database.fetch_all_questions()
    if len(questionsResponse) == 0:
        return jsonify({
            'Message': 'Sorry there are no questions yet!'
        }), 400

    qnJson = json_utility.questions_to_json_list_utilities(questionsResponse)

    return jsonify({
        'Questions': qnJson,
        'Message': 'Questions fetched successfully!'
    }), 200


@mod.route('/questions/<int:questionId>', methods=['DELETE'])
def delete_question(questionId):
    try:
        if database.delete_question(questionId):
                return jsonify({
                    'Message': 'Question deleted!'
                }), 200

    except IndexError:
        return jsonify({
            'Message': 'Question does not exist.'
        }), 400


@mod.route('/questions/users/<string:user_id>', methods=['GET'])
def get_questions_for_user(user_id):
    """
    Function enables a user to fetch all questions
    """
    questions = database.fetch_questions_for_user(user_id)
    if len(questions) == 0:
        return jsonify({
            'Message': 'Sorry there are no questions yet!'
        }), 400
        
    json_questions = json_utility.questions_to_json_list_utilities(questions)
    return jsonify({
        'Questions': json_questions,
        'Message': 'Questions fetched successfully!'
    }), 200