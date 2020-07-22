import os
import unittest
import json
import random
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from flaskr import QUESTIONS_PER_PAGE


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format(
            'postgres:postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['categories']), 0)

    def test_get_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['categories']), 0)
        self.assertGreaterEqual(len(data['questions']), 0)
        self.assertLessEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertGreaterEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], None)

    def test_delete_question(self):
        random_id = random.randint(1, 10)
        res = self.client().delete(f'/api/questions/{random_id}')
        data = json.loads(res.data)

        if res.status_code == 200:
            self.assertTrue(data['success'])
            self.assertTrue(data['deleted_question'])
        elif res.status_code == 404:
            self.assertFalse(data['success'])
            self.assertTrue(data['message'])

    def test_creat_new_question(self):
        mock_question = {
            'question': f'test question {random.randint(0, 1000)}',
            'answer': f'test answer {random.randint(0, 1000)}',
            'category': random.randint(1, 5),
            'difficulty': random.randint(1, 5),
        }
        res = self.client().post('/api/questions', data=json.dumps(mock_question))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['new_question'])

    def test_search_questions(self):
        res = self.client().post(
            '/api/search', data=json.dumps({'searchTerm': 'test'}))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['questions']), 0)
        self.assertLessEqual(len(data['questions']), QUESTIONS_PER_PAGE)
        self.assertGreaterEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], None)

    def test_get_questions_by_category(self):
        random_id = random.randint(1, 10)
        res = self.client().get(f'/api/categories/{random_id}/questions')
        data = json.loads(res.data)

        if res.status_code == 200:
            self.assertTrue(data['success'])
            self.assertGreaterEqual(len(data['questions']), 0)
            self.assertLessEqual(len(data['questions']), QUESTIONS_PER_PAGE)
            self.assertGreaterEqual(data['total_questions'], 0)
            self.assertTrue(data['current_category'])
        elif res.status_code == 404:
            self.assertFalse(data['success'])
            self.assertTrue(data['message'])

    def test_generate_quiz_question(self):
        request_data = {
            'previous_questions': [random.randint(0, 15) for x in range(random.randint(0, 5))],
            'quiz_category': {
                'id': random.randint(1, 5),
                'type': 'test type'
            }
        }
        res = self.client().post('/api/quizzes', data=json.dumps(request_data))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        assert type(data['question']) is (None or dict)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
