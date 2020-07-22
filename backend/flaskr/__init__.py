import os
from flask import Flask, request, abort, jsonify, Response, abort
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
    InternalServerError
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category
from utils import (
    paginate_result,
    format_questions,
    format_categories,
    is_valid_question,
    is_valid_search,
    is_valid_quiz
)

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r'/api//*': {'origins': '*'}})

    @app.after_request
    def allow_cors(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, PATCH, OPTIONS')
        return response

    @app.route('/api')
    def index():
        return jsonify({
            'success': 'true'
        }), 200

    @app.route('/api/categories', methods=['GET'])
    def get_all_categories():
        categories = Category.query.all()
        response = {
            'categories': format_categories(categories),
            'success': True
        }
        return jsonify(response)

    @app.route('/api/questions', methods=['GET'])
    def get_all_questions():
        questions = Question.query.all()
        categories = Category.query.all()
        paginated_result = paginate_result(
            request, format_questions(questions), QUESTIONS_PER_PAGE)
        response = {
            'success': True,
            'questions': paginated_result,
            'total_questions': len(questions),
            'categories': format_categories(categories),
            'current_category': None
        }
        return jsonify(response)

    @app.route('/api/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question_to_be_deleted = Question.query.filter(
                Question.id == id).one_or_none()

            if not question_to_be_deleted:
                raise NotFound()

            question_to_be_deleted.delete()
            response = {
                'success': True,
                'deleted_question': question_to_be_deleted.format()
            }
            return jsonify(response)
        except NotFound as e:
            abort(404)
        except Exception as e:
            abort(500)

    @app.route('/api/questions', methods=['POST'])
    def create_new_question():
        try:
            question_object = json.loads(request.data)

            if (not is_valid_question(question_object)):
                raise BadRequest()

            new_question = Question(**question_object)
            new_question.insert()

            response = {
                'success': True,
                'new_question': new_question.format()
            }
            return jsonify(response)
        except BadRequest as e:
            abort(400)
        except Exception as e:
            abort(500)

    @app.route('/api/search', methods=['POST'])
    def search_questions():
        try:
            request_object = json.loads(request.data)
            if (not is_valid_search(request_object)):
                raise BadRequest()

            search_term = request_object['searchTerm']

            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            paginated_result = paginate_result(
                request, format_questions(questions), QUESTIONS_PER_PAGE)
            response = {
                'success': True,
                'questions': paginated_result,
                'total_questions': len(questions),
                'current_category': None
            }
            return jsonify(response)

        except BadRequest as e:
            abort(400)
        except Exception as e:
            abort(500)

    @app.route('/api/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        try:
            categories = Category.query.all()
            selected_category = Category.query.filter(
                Category.id == id).one_or_none()

            if not selected_category:
                raise NotFound()

            questions = Question.query.filter(
                Question.category == selected_category.id).all()

            paginated_result = paginate_result(
                request, format_questions(questions))
            response = {
                'success': True,
                'questions': paginated_result,
                'total_questions': len(questions),
                'current_category': selected_category.format()
            }
            return jsonify(response)
        except NotFound as e:
            abort(404)
        except Exception as e:
            abort(500)

    @app.route('/api/quizzes', methods=['POST'])
    def generate_quiz_question():
        try:
            request_object = json.loads(request.data)
            if (not is_valid_quiz(request_object)):
                raise BadRequest()

            previous_questions = request_object['previous_questions']
            quiz_category = request_object['quiz_category']
            filter_criteria = {
                'category': Question.category == quiz_category['id'],
                'previous_questions': Question.id.notin_(previous_questions)
            }

            questions = Question.query.filter(filter_criteria['category']) \
                .filter(filter_criteria['previous_questions']).all()

            if len(questions):
                next_question = questions[random.randint(
                    0, len(questions) - 1)].format()
            else:
                next_question = None

            response = {
                'success': True,
                'question': next_question
            }
            return jsonify(response)
        except BadRequest as e:
            abort(400)
        except Exception as e:
            abort(500)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Requested resource not found'
        }), 404

    @app.errorhandler(422)
    def unproccessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Requested resource is unproccessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app
