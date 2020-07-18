# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

(C) 1. Use Flask-CORS to enable cross-domain requests and set response headers. 
(C) 2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
(C) 3. Create an endpoint to handle GET requests for all available categories. 
(C) 4. Create an endpoint to DELETE question using a question ID. 
(C) 5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
(C) 6. Create a POST endpoint to get questions based on category. 
(C) 7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
(C) 8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
(C) 9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
1. GET '/categories'
2. GET '/questions?page=page_nb'
3. GET '/categories/<int:category_id>/questions'
4. POST '/questions'
5. DELETE '/questions/<int:question_id>'
6. POST '/search'
7. POST '/quizzes'

1. GET '/categories'
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}

2. GET '/questions?page=page_nb'
    - Fetches a dictionary of quesitons paginated questions containing id, question, answer, category, difficutly. Total questions and categories are also returned.
    - Request Arguments: 
        - page_nb : int, specifies the page number in pagination; default = 1
    - Returns: A JSON with keys:
        - success : values True otherwise error code is returned
        - questions : dictionary, list of 10 questions (paginated), each question is a dictionary
            with keys:
                - id : int, id of the question
                - question : string, the question statement
                - answer : string, answer to the question
                - category : int, category of 1-6
                - difficulty : int, difficulty levels of 1-5
        - total questions : int, total number of questions
        - categories : dictionary, as described at the GET '/categories' endpoint

    Example:
    {
    "categories": [
        {
        "id": 1,
        "type": "Science"
        },
        ...
        {
        "id": 5,
        "type": "Entertainment"
        },
        {
        "id": 6,
        "type": "Sports"
        }
    ],
    "questions": [
        {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        ...
        {
        "answer": "One",
        "category": 2,
        "difficulty": 4,
        "id": 18,
        "question": "How many paintings did Van Gogh sell in his lifetime?"
        }
    ],
    "success": true,
    "total_questions": 18
    }

3. GET '/categories/<int:category_id>/questions'
    - Fetches a dictionary of paginated questions in a specific category containing id, question, answer, category, difficutly. Total questions and categories are also returned.
    - Request arguments: 
        - category_id : int, specifying the category from which the questions are requested
    - Returns: same format as for GET '/questions' endpoint plus
        - category_id : int, specifying the category from which the questions were requested

4. POST '/questions'
    - Inserts a new question with data from a JSON containing question, answer, difficulty and category
    - Request arguments: JSON in the form:
        {
            'question' : string, question statement
            'answer' : string, answer to the question
            'difficulty' : int, difficulty of the question on a scale of 1-5
            'category' : int, id of the category of the question, [1-6]
        }
    - Returns:
        - success : boolean, True if succeeded aborts with 400 otherwise

5. DELETE '/questions/<int:question_id>'
    - Deletes a question specified by question_id
    - Request arguments:
        - question_id : int, id specifying the question to be deleted
    - Returns:
        - success : boolean, True if succeeded aborts with 404 if question with id 'question_id' not found, 500 if delete was not executed.
        - questions, total_questions: same as described at GET '/questions' endpoint
        - deleted : int, id of the question which was successfully deleted
        - message:

6. POST '/search'
    - Fetches questions that match a search criteria in the format described at GET '/questions' endpoint
    - Request arguments: JSON in the form:
    {
        'searchTerm' : string, search keyword
    }
    - Returns:
        - success : boolean, True if succeeded aborts with 404 if no question matches the criteria
        - questions, total_questions: same as described at GET '/questions' endpoint

7. POST '/quizzes'
    - Fetches randomized and unique (in a gameplay session) individual questions to play a quizz. Returns a dictionary containing question, answer, difficulty and category
    - Request arguments: JSON in the form:
    {
        'quiz_category' : dictionary { 'id' : int, 'type' string } specifies the category if questions should be fetched from a category; if is sent { 'id' : 0, 'type' : click } the endpoint returns randomized questions from all categories. 
        'previous_questions' : array of int, ids of questions that were already shown in the quizz
    }
    - Returns:
        - success : boolean, True if succeeded aborts with 404 if no question matches the criteria
        - question : dictionary containing question statement, answer, difficulty and category as described at GET '/questions' endpoint. If there are no more unique questions an empty string is returned ''

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```