### Hello in my chat app

#### I made this app using these technologies
- `Python`
- `Django`
- `sqlite3 for development and PostgreSQL for the production`
- `HTML, CSS, JS for the frontent`
- `Django channels from creating the websockets`
- `Make for professional automation`
#### You can run these commands to run the project locally in your local machiene using make

```
make install
make collectstatic
make migrate
make run
```

And then open this URL in your browser `127.0.0.1:8000` and you should see the website in your browser

And you can run these commands if you don't have make in your local machiene

#### for windows
``` 
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collecstatic --noinput
python manage.py runserver
```
#### For linux and mac
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collecstatic --noinput
python3 manage.py runserver
```
