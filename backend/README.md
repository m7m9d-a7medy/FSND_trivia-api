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


## Documentation

### Endpoints
All endpoints are behind static prefix ```/api``` to avoid any conflicts with localhosts

- ```GET '/api/categories'```
- ```GET '/api/questions'```
- ```DELETE '/api/questions/<id>'```
- ```POST '/api/questions'```
- ```GET '/api/categories/<id>/questions'```
- ```POST '/api/search'```
- ```POST '/api/quizzes'```

All endpoints returns ```success``` boolean key in response which indicates if the operation has completed successfuly. 

**GET '/categories'**
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of key value pairs. 
    
- Sample: `curl -X GET http://127.0.0.1:5000/api/categories`
    ```json
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "success": true
    }
    ```

**GET '/api/questions?page=<page_number>'**
- Fetches a list of all questions, paginated for optimizations 10 questions per page
- Request Arguments:
    - page_number: The corresponding page number
- Returns:
    - A list of questions, maximum 10 per request. 
    - Total number of questions.
    - An object containing categories.
- Sample: `curl -X GET http://127.0.0.1:5000/api/questions?page=1`
    ```json
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "current_category": null,
        "questions": [
            {
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
            },
            {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            },
            {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            },
            {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            },
            {
                "answer": "Brazil",
                "category": 6,
                "difficulty": 3,
                "id": 10,
                "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
                "answer": "Uruguay",
                "category": 6,
                "difficulty": 4,
                "id": 11,
                "question": "Which country won the first ever soccer World Cup in 1930?"
            },
            {
                "answer": "George Washington Carver",
                "category": 4,
                "difficulty": 2,
                "id": 12,
                "question": "Who invented Peanut Butter?"
            },
            {
                "answer": "Lake Victoria",
                "category": 3,
                "difficulty": 2,
                "id": 13,
                "question": "What is the largest lake in Africa?"
            },
            {
                "answer": "The Palace of Versailles",
                "category": 3,
                "difficulty": 3,
                "id": 14,
                "question": "In which royal palace would you find the Hall of Mirrors?"
            }
        ],
        "success": true,
        "total_questions": 21
    }
    ```

**DELETE '/api/questions/<id>'**
- Deletes the question with the specific ID
- Request Arguments:
    - id: The corresponding id of the question to be deleted
- Returns:
    - An instance of the question if successful along with status code 200.
    - Returns an error message if the operation wasn't successful along with status code of the error.
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/questions/1`

    Success
    ```json
    {
        "deleted_question": {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        "success": true
    }
    ```
    Fail
    ```json
    {
        "error": 404,
        "message": "Requested resource not found",
        "success": false
    }
    ```

**POST '/api/questions'**
- Create a new question based on the payload
- Request Arguments:
    - question: question text
    - answer: answer text
    - difficulty: difficulty value where larger is harder
    - category: the id of the category
- Returns:
    - An instance of the question if successful along with status code 200.
    - Returns an error message if the operation wasn't successful along with status code of the error.
- Sample: ``

    Success
    ```json
    {
        "new_question": {
            "answer": "Dhoni",
            "category": 6,
            "difficulty": 3,
            "id": 24,
            "question": "Who is most successful captain in ICC trophies?"
        },
        "success": true
    }
    ```
    Fail
    ```json
    {
        "error": 500,
        "message": "Internal server error",
        "success": false
    }
    ```

**GET '/api/categories/< id >/questions?page=< page_number >'**
- Fetches a list of questions with a specific category, paginated for optimizations 10 questions per page
- Request Arguments:
    - id: ID of the category
    - page_number: The corresponding page number
- Returns:
    - A list of questions, maximum 10 per request. 
    - Total number of questions.
    - An object containing categories.
- Sample `curl -X GET http://127.0.0.1:5000/api/categories/1/questions?page=1`
    ```json
    {
        "current_category": {
            "id": 1,
            "type": "Science"
        },
        "questions": [
            {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
            },
            {
                "answer": "Alexander Fleming",
                "category": 1,
                "difficulty": 3,
                "id": 21,
                "question": "Who discovered penicillin?"
            },
            {
                "answer": "Blood",
                "category": 1,
                "difficulty": 4,
                "id": 22,
                "question": "Hematology is a branch of medicine involving the study of what?"
            }
        ],
        "success": true,
        "total_questions": 3
    }
    ```

**POST '/api/search?page=< page_number >'**
- Fetches a list of questions which matches a search term, paginated for optimizations 10 questions per page
- Request Arguments:
    - searchTerm: Search term
    - page_number: The corresponding page number
- Returns:
    - A list of questions, maximum 10 per request. 
    - Total number of questions.
    - An object containing categories.
- Sample: `curl -X POST http://127.0.0.1:5000/api/search?page=1 -H "Content-Type: application/json" -d "{ \"searchTerm\": \"box\" }"`
    ```json
    {
        "current_category": null,
        "questions": [
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
            }
        ],
        "success": true,
        "total_questions": 1
    }
    ```

**POST '/api/quizzes'**
- Fetches a random question not present within the previously asked questions
- Request Arguments:
    - previous_questions: a list of integers representing the IDs of the previously asked questions
    - quiz_category: a category object
- Returns: A unique and random question within the specific category
- Sample: `curl -X POST http://127.0.0.1:5000/api/quizzes -H "Content-Type: application/json" -d "{\"quiz_category\":{\"id\":1,\"type\":\"Science\"},\"previous_questions\":[0]}"`
    ```json
    {
        "question": {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        "success": true
    }
    ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```