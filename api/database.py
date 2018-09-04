import psycopg2
from pprint import pprint
from datetime import datetime

class DatabaseConnection:
    try:
        def __init__(self):
            self.connection = psycopg2.connect(
                """
                dbname='stackoverflowlite' user='postgres' password='qwerty'
                host='localhost' port='5432'
                """
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            pprint("Connected!")

    except:
        pprint("Failed To Connect to Database")

    def create_user(self, user_id, username, email, password):
        createdOn = datetime.now()
        insert_user_command = """
        INSERT INTO stackoverflow.users VALUES ('{}', '{}', '{}', '{}', '{}') RETURNING "userId";
        """.format(user_id,username, email, password, createdOn)
        self.cursor.execute(insert_user_command)
        user = self.cursor.rowcount
        return user

    def fetch_user_by_username(self, username):
        get_user_command = """
        SELECT * FROM stackoverflow.users WHERE "username"= '{}';
        """.format(username)
        self.cursor.execute(get_user_command)

        user = self.cursor.fetchone()
        return user

    def fetch_user_by_email(self, email_address):
        get_user_by_email_command = """
        SELECT * FROM stackoverflow.users WHERE "email"='{}'
        """.format(email_address)
        self.cursor.execute(get_user_by_email_command)

        user = self.cursor.fetchone()
        return user

    def fetch_user_by_username_password(self, username, password):
        get_user_command = """
        SELECT * FROM  stackoverflow.users WHERE "username"='{}' AND "password"='{}'
        """.format(username, password)
        print(get_user_command)
        self.cursor.execute(get_user_command)

        user = self.cursor.fetchone()
        return user

    def fetch_username(self, username):
        get_user_command = """
        SELECT username FROM  stackoverflow.users WHERE username='{}' 
        """.format(username)
        self.cursor.execute(get_user_command)

        user = self.cursor.fetchone()
        return user

    def create_question(self, user_id, question):
        createdOn = datetime.now()
        create_question_command = """
        INSERT INTO stackoverflow.questions ("userId", "question", "createdOn") VALUES ('{}', '{}', '{}') RETURNING "questionId"
        """.format(user_id, question, createdOn)
        self.cursor.execute(create_question_command)
        question = self.cursor.fetchone()[0]
        return question

    def update_question(self, user_id, question_id, question):
        update_question_command = """UPDATE stackoverflow.questions SET question=%s\
                WHERE userId=%s AND questionId=%s;
                """
        self.cursor.execute(update_question_command, [question, user_id[0], question_id])

    def fetch_question_by_id(self, question_id):
        fetch_question_command = """
        SELECT * FROM stackoverflow.questions WHERE "questionId" = '{}'
        """.format(question_id)
        self.cursor.execute(fetch_question_command)

        question = self.cursor.fetchone()
        return question

    def fetch_questions_for_user(self, user_id):
        fetch_user_question_command = """
        SELECT * FROM stackoverflow.questions WHERE "userId" = '{}'
        """.format(user_id)
        self.cursor.execute(fetch_user_question_command)

        questions = self.cursor.fetchall()
        return questions

    def fetch_all_questions(self):
        fetch_all_questions_command = """
        SELECT * FROM stackoverflow.questions
        """
        self.cursor.execute(fetch_all_questions_command)
        
        questions = self.cursor.fetchall()
        print(questions)
        return questions

    def fetch_question_for_user(self, user_id, question_id):
        fetch_user_question_command = """
        SELECT * FROM stackoverflow.questions WHERE "userId" = '{}' AND questions.questionId='{}'
        """.format(user_id, question_id)
        self.cursor.execute(fetch_user_question_command)

        question = self.cursor.fetchone()
        return question

    def insert_answer_for_question(self, user_id, question_id, answer):
        createdOn = datetime.now()
        create_answer_command = """
        INSERT INTO stackoverflow.answers ("userId", "questionId", "answer", "createdOn") VALUES ('{}','{}','{}', '{}') RETURNING "answerId"
        """.format(user_id, question_id, answer, createdOn)
        print(create_answer_command)
        self.cursor.execute(create_answer_command)

        ans = self.cursor.fetchone()[0]
        return ans


    def fetch_answers_for_question(self, question_id):
        fetch_answer_command = """
        SELECT * FROM stackoverflow.answers WHERE "questionId" = '{}'
        """.format(question_id)
        self.cursor.execute(fetch_answer_command)
        answers = self.cursor.fetchall()
        return answers

    def fetch_answers_by_id(self, answer_id):
        fetch_answer_command = """
        SELECT * FROM stackoverflow.answers WHERE "answerId" = '{}'
        """.format(answer_id)
        self.cursor.execute(fetch_answer_command)
        answer = self.cursor.fetchone()
        return answer
    
    def fetch_answers_for_question_for_user(self, question_id, user_id):
        fetch_answer_command = """
        SELECT * FROM stackoverflow.answers WHERE "questionId" = '{}'
        """.format(question_id)
        self.cursor.execute(fetch_answer_command)

        answers = self.cursor.fetchall()
        return answers

    def delete_question(self, question_id):
        delete_question_command = """
        DELETE FROM stackoverflow.questions WHERE "questionId" = '{}'
        """.format(question_id)

        delete_answer_command ="""
        DELETE FROM stackoverflow.answers WHERE "questionId" = '{}';
        """.format(question_id)

        self.cursor.execute(delete_answer_command)
        self.cursor.execute(delete_question_command)
        qn = self.cursor.rowcount
        return qn

    def delete_answer(self, answer_id):
        delete_answer_command = """
        DELETE FROM stackoverflow.answers WHERE "answerId" = '{}'
        """.format(answer_id)

        self.cursor.execute(delete_answer_command)

