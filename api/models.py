from datetime import date

from flask import jsonify
from api.database import DatabaseConnection
import re
from passlib.hash import pbkdf2_sha256 as sha256

users = []
questions = []
answers = []

database = DatabaseConnection()


class User:
    def __init__(self, userId, username, email, password):
        self.userId = userId
        self.username = username
        self.email = email
        self.password = password

    def generate_password_hash(self):
        return sha256.hash(self.password)

    @staticmethod
    def verify_password_hash(password, password_hash):
        return sha256.verify(password, password_hash)


class Question:
    def __init__(self, userId, question):
        self.userId = userId
        # self.questionId = questionId
        self.question = question

    def add_question(self):
        qn = database.create_question(self.userId, self.question)
        if qn is None:
            return False
        return qn

    @staticmethod
    def fetch_all_questions():
        qn = database.fetch_all_questions()
        if qn is None:
            return None
        return qn

    @staticmethod
    def fetch_user_question(user_id, question_id):
        qn = database.fetch_question_for_user(user_id, question_id)
        if qn is None:
            return None
        return qn

    @staticmethod
    def fetch_answers_for_question(question_id):
        ans = database.fetch_answers_for_question(question_id)
        if ans is None:
            return False
        return ans

    @staticmethod
    def fetch_question(question_id):
        qn = database.fetch_question_by_id(question_id)
        if qn is None:
            return None
        return qn

    @staticmethod
    def fetch_questions_for_user(user_id, question_id):
        qns = database.fetch_question_for_user(user_id, question_id)
        if qns is None:
            return None
        return qns

    def update_question(self, question_id, details):
        database.update_question(self.userId, question_id, details)

        qn = database.fetch_question_for_user(self.userId, question_id)

        return qn


class Answer:
    def __init__(self, user_id, question_id, answer_id, answer):
        self.answerId = answer_id
        self.question_id = question_id
        self.answer = answer
        self.user_id = user_id
        self.accepted = False

    @staticmethod
    def fetch_answers(question_id):
        ans = database.fetch_answers_for_question(question_id)
        if ans is None:
            return None

        return ans
    
    def fetch_answers_for_user(self, user_id, question_id):
        ans = database.fetch_answers_for_question_for_user(user_id, question_id)