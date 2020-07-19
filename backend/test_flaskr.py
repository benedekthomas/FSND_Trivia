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
        self.database_path = "postgres://benedekthomas:password1@{}/{}"\
                             .format('127.0.0.1:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    # Tests for the GET /questions endpoint.
    # error handling behavior test is not applicable, it would require the
    # setup of an empty database.

    def test_getPaginatedQuestions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    # Test for the POST /questsions endpoint.
    # - Functional test: adds a well formatted question to the database.
    # - Error handling test: sends an empty JSON, tests for 500 response.

    def test_postNewQuestion_functional(self):
        """
        Tests functional behavior of POST /questions endpoint
            -- add new question with right syntax
        """
        new_question = {
            'question': 'Test question?',
            'answer': 'It is a test!',
            'difficulty': 1,
            'category': 1
        }

        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_postNewQuestion_err(self):
        """
        Tests error handling behavior of POST /questions endpoint
            -- add new question with bad syntax
        """
        new_question = {
        }

        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)

    # Tests for the GET /categories/cat_id/questions endpoint
    # - Funcational test: iterates through all categories and retrieves
    #                   questions in that category.
    # - Error handling test: requests questions for a non-existing category

    def test_getQuestionsByCategory_functional(self):
        category_ids = [
            cat.id for cat in Category.query.order_by(Category.id).all()]

        for id in category_ids:
            response = self.client().get('/categories/' + str(id) +
                                         '/questions')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(len(data['questions']))
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['current_category'])
            self.assertTrue(len(data['categories']))

    def test_getQuestionsByCategory_functional(self):
        response = self.client().get('/categories/7/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    # Test for GET /categories endpoint
    def test_getCategories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    # Tests POST /search endpoint
    # - Functional test: search for the term 'what' gives guarnteed response
    # - Error handling test: search for a term which gives no response
    def test_search_functional(self):
        searchTerm = {
            'searchTerm': 'What'
        }
        response = self.client().post('/search', json=searchTerm)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_search_err(self):
        searchTerm = {
            'searchTerm': '123456789'
        }
        response = self.client().post('/search', json=searchTerm)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Tests for POST /quizzes endpoint
    def test_quiz_questions(self):
        quizParams = {
            'previous_questions': '[]',
            'quiz_category': {
                'id': 0,
                'type': 'click',
            }
        }
        response = self.client().post('/quizzes', json=quizParams)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_quiz_questions_err(self):
        quizParams = {
            "previous_questions": "[]",
            "quiz_category": {
                "id": "7",
                "type": "Non-existent",
            }
        }
        response = self.client().post('/quizzes', json=quizParams)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def tearDown(self):
        """Executed after reach test"""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
