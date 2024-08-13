## To launch: (example on linux)

Env:
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`

Back & front:
1. `cd inputs`
2. `python manage.py migrate`
3. `python manage.py runserver`

In second terminal:
1. `cd frontend`
2. `npm install axios`
3. `npm start`
