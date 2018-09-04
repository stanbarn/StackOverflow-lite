import unittest
import json
from api import app


class TestApiEndPoints(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_registration_username_with_space(self):
        user = dict(
            username=" ",
            email="stanleybarna@gmail.com",
            password="YTH123k6"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Sorry, enter your username!")

    def test_registration_username_empty_string(self):
        user = dict(
            username="",
            email="stanleybarna@gmail.com",
            password="YTH123k6"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Sorry, enter your username!")

    def test_registration_username_is_registered_to_another_user(self):
        user = dict(
            username="barnabas",
            email="stanleybarna@gmail.com",
            password="YTH123k6"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Sorry, that username is registered to another user!")

    def test_registration_email_with_empty_string(self):
        user = dict(
            username="nagwere",
            email="",
            password="YTH123k6"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Sorry, enter your email!")

    def test_registration_email_with_space(self):
        user = dict(
            username="nagwere",
            email=" ",
            password="YTH123k6"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Sorry, enter your email!")

    def test_that_registration_email_is_invalid(self):
        user = dict(
            username="nagwere",
            email="test..gmail.co",
            password="YTH123k6"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Invalid email address!")

    def test_registration_email_is_registered_to_another_user(self):
        user = dict(
            username="nagwere",
            email="stanleybarna@gmail.com",
            password="Ths123456"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Sorry, that email is registered to another user!")

    def test_registration_password_with_empty_string(self):
        user = dict(
            username="nagwere",
            email="nagwere@gmail.com",
            password=""
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Sorry, you did not enter your password!")

    def test_registration_password_with_space(self):
        user = dict(
            username="nagwere",
            email="nagwere@gmail.com",
            password=" "
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Sorry, you did not enter your password!")

    def test_registration_password_with_only_numerics(self):
        user = dict(
            username="nagwere",
            email="nagwere@gmail.com",
            password="1234567"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Passwords should include upper, lower cases, and numeric characters")

    def test_registration_password_with_no_uppercase_characters(self):
        user = dict(
            username="nagwere",
            email="nagwere@gmail.com",
            password="wer4567"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Passwords should include upper, lower cases, and numeric characters")

    def test_registration_password_with_no_lowercase_characters(self):
        user = dict(
            username="nagwere",
            email="nagwere@gmail.com",
            password="TTN4567"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Passwords should include upper, lower cases, and numeric characters")

    def test_registration_password_less_than_six_characters(self):
        user = dict(
            username="nagwere",
            email="nagwere@gmail.com",
            password="Twer4"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Passwords should be at least 6 characters long!")

    def test_that_password_is_correct(self):
        user = dict(
            username="nagwere",
            email="nagwere@gmail.com",
            password="Tes1234567"
        )

        response = self.tester.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply["Message"], "nagwere has registered successfully")

    def test_that_can_signin_with_username_with_empty_string(self):
        user = dict(
            username="",
            password="Twer4"
        )

        response = self.tester.post(
            'api/v1/signin',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "You did not enter your username!")

    def test_that_can_signin_with_username_with_space(self):
        user = dict(
            username=" ",
            password="Twer4"
        )

        response = self.tester.post(
            'api/v1/signin',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "You did not enter your username!")

    def test_that_can_signin_with_password_with_empty_string(self):
        user = dict(
            username="nagwere",
            password=" "
        )

        response = self.tester.post(
            'api/v1/signin',
            content_type='application/json',
            data=json.dumps(user)
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "You did not enter your password!")

    def test_that_can_signin_with_password_with_empty_string(self):
        user = dict(
            username="nagwere",
            password=""
        )

        response = self.tester.post(
            'api/v1/signin',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "You did not enter your password!")

    def test_that_can_signin_with_username_that_is_not_registered_on_platform(self):
        user = dict(
            username="brianT",
            password="Twer4"
        )

        response = self.tester.post(
            'api/v1/signin',
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["Message"], "Sorry, Failed  authentication. Username does not exist!")

    def test_that_can_add_question(self):
        question = dict(
            question='test answer with unit test',
            userId='d32c7951-2d28-43d1-b9ad-93f096982be2'
        )
        response = self.tester.post(
            'api/v1/questions/questions',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply["Message"], "Question added successfully!")

    def test_add_question_empty_string(self):
        question = dict(
            question='',
            userId='d32c7951-2d28-43d1-b9ad-93f096982be2'
        )
        response = self.tester.post(
            'api/v1/questions/questions',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply["Message"], "Sorry, you didn't enter any question!")

    def test_add_question_with_space(self):
        question = dict(
            question=' ',
            userId='d32c7951-2d28-43d1-b9ad-93f096982be2'
        )
        response = self.tester.post(
            'api/v1/questions/questions',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply["Message"], "Sorry, you didn't enter any question!")

    def test_get_one_question(self):

        response = self.tester.get(
            'api/v1/questions/25',
            content_type='applcation/json',
        )

        self.assertEqual(response.status_code, 200)

    def test_that_can_add_answer_to_question(self):
        question = dict(
            questionId=20,
            userId='d32c7951-2d28-43d1-b9ad-93f096982be2',
            answer='This is a unit test answer'
        )
        response = self.tester.post(
            'api/v1/questions/25/answers',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply["Message"], "Answer added succesfully!")

    def test_add_answer_with_empty_string(self):
        question = dict(
            questionId=25,
            userId='d32c7951-2d28-43d1-b9ad-93f096982be2',
            answer=''
        )
        response = self.tester.post(
            'api/v1/questions/13/answers',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply["Message"], "Sorry, you did not enter any answer!")

    def test_add_answer_with_space(self):
        question = dict(
            questionId=25,
            userId='d32c7951-2d28-43d1-b9ad-93f096982be2',
            answer=' '
        )
        response = self.tester.post(
            'api/v1/questions/13/answers',
            content_type='application/json',
            data=json.dumps(question)
        )
        reply = json.loads(response.data.decode())

        self.assertEqual(reply["Message"], "Sorry, you did not enter any answer!")

    def test_get_answers_for_question_that_does_not_exist(self):

        response = self.tester.get(
            'api/v1/questions/questions/answers/113',
            content_type='applcation/json'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply["Message"], "Question does not exist.")

    def test_get_answers_for_question(self):

        response = self.tester.get(
            'api/v1/questions/questions/answers/25',
            content_type='applcation/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_get_questions_for_user(self):

        response = self.tester.get(
            'api/v1/questions/questions/users/d32c7951-2d28-43d1-b9ad-93f096982be2',
            content_type='applcation/json',
        )

        self.assertEqual(response.status_code, 200)

    def test_get_all_questions(self):

        response = self.tester.get(
            'api/v1/questions/questions',
            content_type='applcation/json',
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_question(self):

        response = self.tester.delete(
            'api/v1/questions/questions/20',
            content_type='applcation/json',
        )

        self.assertEqual(response.status_code, 200)
