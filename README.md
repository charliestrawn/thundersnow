# Payment Tracker

Simple Flask + Angular 1.4 app for tracking and reporting on weekly payments. I use this project to learn and experiment with different frontend and backend languages/frameworks/technologies, and the next iteration will likely be react/redux.

### TODOs
- [ ] More unit tests
- [ ] Add more TODOs

### Developing

Make sure you have Python 3 and Postgres installed. I'd also recommend [virtualenv]() and [virtualenvwrapper]().

- Fork or clone the repo
- cd into repo
- `mkvirtualenv thundersnow -a $PWD`
- `pip install -Ur requirements_dev.txt`
- export environment varialbes (for convenience I like to save these in `~/.virtualenvs/thundersnow/bin/postactivate` so they sourced every time I `workon thundersnow`)

```bash
export DATABASE_URL="postgresql://localhost/thundersnow"
export ADMIN_EMAIL="test@test.com"
export ADMIN_PASSWORD="testytest"
export SECRET_KEY="myprecious"
```

- Create the database `python manage.py create_db`
- Create your user `python manage.py create_admin`
- Start the app `python manage.py runserver`
- Profit! Head to localhost:5000 and login to start entering payments.

### Testing

- Setup TravisCI

### Deploying

- Heroku
