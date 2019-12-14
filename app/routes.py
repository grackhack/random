from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from flask import render_template, flash, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from app import app
from app import db
from app.forms import LoginForm
from app.models import Game
from config import Config


def build_plot():
    df = pd.read_sql_query("""select date, de1, de2,de3,de4,de5,de6,
                                    de7, de8,de9,de10,de11,de12,
                                    de13, de14,de15,de13,de17,de18,
                                    de19, de20,de21,de22,de23,de24
                                   from game order by date desc
                                   """, Config.SQLALCHEMY_DATABASE_URI, index_col='date')
    df = df.fillna(-1)
    df = df.replace(True, 1)
    fig = plt.gcf()
    fig.set_size_inches(20, 10)
    ax = plt.gca()
    df.cumsum().plot(kind='line', ax=ax, grid=True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig('new_plot.png', ax=ax)


def get_play_history(row: List[int]) -> List[str]:
    ng = False
    res = []
    cnt = 1
    for i in row:
        if i == 0 and not ng:
            cnt = 1
            ng = True
            res.append(str(cnt))
        elif i == 0 and ng:
            cnt += 1
            res.append(str(cnt))
        else:
            res.append('•')
            ng = False
    return res[::-1]


def get_digit_row(digit):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    connection = engine.raw_connection()
    df = pd.read_sql_query("""
        select de{}
        from game order by date limit 500;        
        """.format(digit), connection)
    df = df.fillna(0)
    row = df.replace(True, 1)[f'de{digit}'].tolist()
    history = get_play_history(row)

    return history


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

    max_date = db.session.query(db.func.max(Game.date)).scalar()
    dates = db.session.query(Game.date).order_by(Game.date.desc()).limit(500)
    # build_plot()
    games = []
    result = []
    for digit in range(1, 25):
        result = get_digit_row(digit)
        games.append({'digit': f'{digit:3}', 'game': result})
    return render_template('index.html', title='Stat', user=user, max_date=max_date, games=games,
                           url='new_plot.png', count_games=len(result), dates=dates)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Привет, бро! remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
