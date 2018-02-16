# PlatyPlus API

Create a virtual environment:
```bash
python3.6 -m venv env
source venv/bin/activate
```

Install everything needed:
```bash
pip install -r requirements/requirements.txt
```

Create the database and run the server:
```
python manage.py migrate
python manage.py runserver
```

You should be able to access the server on [here](http://localhost:8000/graphql).
