# LITREVIEW

LITReview is a Django application designed to facilitate the management and review of books. It allows users to create, edit, and delete reviews and books, and follow other users. Users can also search for books and view profiles of other users.


## Setup

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the dependencies: `pip install -r requirements.txt`

Make sure the database migrations are applied: `python manage.py migrate`.

Load fixture data: `python manage.py loaddata fixtures/initial_data.json`.

Run the server with `python manage.py runserver`.

Navigate to `http://localhost:8000/`.

## Login Credentials

- Username: `testuser`
- Password: `octest12`