import matplotlib.pyplot as plt
import pandas as pd
from flask import render_template, flash, redirect, url_for

from app import app
from app.forms import LoginForm
from app.models import Game
from config import Config


def build_plot():
    df = pd.read_sql_query("""select date, de1, de2,de3,de4,de5,de6,
                                    de7, de8,de9,de10,de11,de12,
                                    de13, de14,de15,de13,de17,de18,
                                    de19, de20,de21,de22,de23,de24
                                   from game order by date
                                   """, Config.SQLALCHEMY_DATABASE_URI, index_col='date')
    df = df.fillna(-1)
    df = df.replace(True, 1)
    fig = plt.gcf()
    fig.set_size_inches(20, 10)
    ax = plt.gca()
    df.cumsum().plot(kind='line', ax=ax, grid=True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(app.static_folder + '/images/new_plot.png', ax=ax)


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

    games = Game.query.all()
    build_plot()
    return render_template('index.html', title='Home', user=user, posts=posts, games=games,
                           url='new_plot.png')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'{form.username.data} Привет, бро! remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
