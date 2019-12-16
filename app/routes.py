import datetime
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from flask import render_template, flash, redirect, url_for, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from app import app
from app import db
from app.forms import LoginForm
from app.models import Game
from app.work_with_games import refresh_game_stat, get_digit_info
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


def get_play_history(row: List[int], positive=True) -> List[str]:
    play = 0 if positive == '1' else 1
    ng = False
    res = []
    cnt = 1
    for i in row:
        if i == play and not ng:
            cnt = 1
            ng = True
            res.append(str(cnt))
        elif i == play and ng:
            cnt += 1
            res.append(str(cnt))
        else:
            res.append('•')
            ng = False
    return res[::-1]


def get_digit_row(digit, play):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    connection = engine.raw_connection()
    df = pd.read_sql_query("""
        select de{d:} from (select date,de{d:}  from game order by date desc limit 500) a order by date;       
        """.format(d=digit), connection)
    df = df.fillna(0)
    row = df.replace(True, 1)[f'de{digit}'].tolist()
    history = get_play_history(row, positive=play)

    return history


@app.route('/')
@app.route('/index')
def index():
    play = request.args.get('play', '1')
    max_date = db.session.query(db.func.max(Game.date)).scalar()
    dates = db.session.query(Game.date).order_by(Game.date.desc()).limit(500)
    # build_plot()
    games = []
    result = []
    for digit in range(1, 25):
        result = get_digit_row(digit, play)
        games.append({'digit': digit, 'game': result})
    return render_template('index.html', title='Stat', max_date=max_date, games=games,
                           url='new_plot.png', count_games=len(result), dates=dates, play=play)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Привет, бро! remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/collect_games', methods=['POST'])
def collect_games():
    try:
        date = request.values.get('day', datetime.datetime.now().strftime("%d.%m.%Y"))
        refresh_game_stat(date)
    except:
        return jsonify({'data': 'error'})
    return jsonify({'data': 'ok'})


@app.route('/settings')
def settings():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    result = engine.execute("""
    select COUNT(*) as count, date_trunc('day', date) as day FROM game GROUP BY day ORDER BY day desc
    """)
    rows = result.fetchall()

    return render_template('settings.html', result=rows)


@app.route('/get_info', methods=['POST'])
def get_info():
    try:
        digit = request.values.get('digit').strip()
        series = get_digit_info(digit)
        stat = render_template('stat.html', series=series)
    except:
        return jsonify({'data': 'error'})
    return jsonify({'stat': stat})


@app.route('/charts')
def charts():
    return render_template('charts.html')
