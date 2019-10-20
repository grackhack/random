from flask import render_template, flash, redirect, url_for

from app import app
from app.forms import LoginForm
from app.models import Game


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    games = {'date': '23.12.12'}
    # games = Game.query.all()
    # print('*' * 30, games, '*' * 30, )
    return render_template('index.html', title='Home', user=user, posts=posts, games=games)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'{form.username.data} Привет, бро! remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
