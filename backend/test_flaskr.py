import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://benedekthomas:password1@{}/{}".format('127.0.0.1:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def test_getPaginatedQuestions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        # self.assertTrue(data['current_category'])
        self.assertTrue(len(data['categories']))

    def test_getQuestionsByCategory(self):
        category_ids = [cat.id for cat in Category.query.order_by(Category.id).all()]

        for id in category_ids:
            response = self.client().get('/categories/' + str(id) + '/questions')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['questions']))
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['current_category'])
            self.assertTrue(len(data['categories']))

    def test_postNewQuestion(self):
        new_question = {
            'question' : 'Test question?',
            'answer' : 'It is a test!',
            'difficulty' : 1,
            'category' : 1
        }

        response = self.client().post('/questions', json = new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_getCategories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()