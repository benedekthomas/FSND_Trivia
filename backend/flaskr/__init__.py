from models import setup_db, Question, Category
import random
from flask_cors import CORS
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
SQLAlchemyError


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    '''
    Sets up CORS for the app. Allows for GET, POST and DELETES methods
    from any origin
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,\
            Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,\
            DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        '''
        Create an endpoint to handle GET requests
        for all available categories.
        '''
        categories = [category.format() for category in
                      Category.query.order_by(Category.id).all()]

        return jsonify({
            'success': True,
            'categories': categories,
        })

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        '''
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of
        the screen for three pages. Clicking on the page numbers
        should update the questions.
        '''
        selection = Question.query.order_by(Question.id).all()
        categories = [category.format() for category in
                      Category.query.order_by(Category.id).all()]
        current_questions = []
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories,
        })

    @app.route('/questions', methods=['POST'])
    def post_new_question():
        '''
        Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of the last
        page of the questions list in the "List" tab.
        '''
        new_question = Question(
            question=request.json.get('question', ''),
            answer=request.json.get('answer', ''),
            difficulty=request.json.get('difficulty', ''),
            category=request.json.get('category', '')
        )

        try:
            new_question.insert()
        except SQLAlchemyError:
            abort(500)

        return jsonify({
            'success': True
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        '''
        Create an endpoint to DELETE question using a question ID.

        TEST: When you click the trash icon next to a question, the
        question will be removed. This removal will persist in the
        database and when you refresh the page.
        '''
        question = Question.query.filter_by(id=question_id).one_or_none()

        if question:
            try:
                question.delete()
            except SQLAlchemyError:
                abort(500)
        else:
            abort(404)

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'deleted': question_id,
        })

    @app.route('/search', methods=['POST'])
    def retrieve_questions_by_search():
        '''
        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
        '''
        searchTerm = request.json.get('searchTerm', '')
        searchTerm = "%" + searchTerm.lower() + "%"

        selection = Question.query.filter(Question.question.
                                          ilike(searchTerm)).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
        })

    @app.route('/categories/<int:cat_id>/questions')
    def retrieve_questions_by_category(cat_id, METHODS=['GET']):
        '''
        Create a GET endpoint to get questions based on category.

        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
        '''
        categories = [category.format()
                      for category in
                      Category.query.order_by(Category.id).all()]
        category_ids = set([int(category['id']) for category in categories])

        # check if cat_id is pointing to a valid category
        if int(cat_id) not in category_ids:
            abort(400)

        selection = Question.query.order_by(
            Question.id).filter_by(category=cat_id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories,
            'current_category': cat_id,
        })

    @app.route('/quizzes', methods=['POST'])
    def retrieve_quiz_questions():
        '''
        Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.

        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not.
        '''
        category = request.json.get('quiz_category', 0)
        previous_questions = set(request.json.get('previous_questions', 0))

        categories = [category.format()
                      for category in
                      Category.query.order_by(Category.id).all()]
        category_ids = set([int(category['id']) for category in categories])

        # check if cat_id is pointing to a valid category
        # +1 because the react app uses the index number instead of id
        if (int(category['id'])+1) not in category_ids:
            abort(400)

        # select questions based on category or all for 0
        if category['type'] == 'click' or category == 0:
            questions = [question.format() for question in
                         Question.query.order_by(Question.id).all()]
        else:
            questions = [question.format() for question in
                         Question.query.order_by(Question.id).
                         filter_by(category=(int(category['id'])+1)).all()]

        # remove previous questions
        questions = [
            question for question in questions if question['id']
            not in previous_questions]

        # select random question out of the collection
        if len(questions):
            question = questions[random.randint(0, len(questions)-1)]
        else:
            question = ''

        return jsonify({
            'success': True,
            'question': question
        })

    # Create error handlers for all expected errors
    # including 404 and 422.

    @app.errorhandler(400)
    def err_bad_request(e):
        return jsonify({
            'success': False,
            'message': 'Bad request',
            'error': 400,
        }), 400

    @app.errorhandler(404)
    def err_resource_not_found(e):
        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'error': 404,
        }), 404

    @app.errorhandler(422)
    def err_unprocessable_entity(e):
        return jsonify({
            'success': False,
            'message': 'Server was not able to process the instructions',
            'error': 422,
        }), 422

    @app.errorhandler(500)
    def err_unauthorized_access(e):
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': 500,
        }), 500

    return app
