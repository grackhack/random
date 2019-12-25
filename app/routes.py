import datetime
from datetime import timezone, timedelta
from random import random
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import login_required
from flask_login import current_user, login_user, logout_user
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from app import app
from app import db
from app import constants
from app.forms import LoginForm, RegistrationForm
from app.models import Game, User, Play, PlayGame
from app.work_with_games import refresh_game_stat, get_digit_info, get_diff_series, get_count_series, calculate_bets, \
    get_balance, get_all_balance, get_all_trend
from config import Config


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=str(random()), balance=10000)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла уcпешно!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


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
        select de{d:} from (select date,de{d:}  from game order by date desc limit {tbl:}) a order by date;       
        """.format(d=digit, tbl=constants.TBL_COL), connection)
    df = df.fillna(0)
    row = df.replace(True, 1)[f'de{digit}'].tolist()
    history = get_play_history(row, positive=play)

    return history


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user.id
    balance = round(get_balance(user),2)
    play = request.args.get('play', '1')
    max_date = db.session.query(db.func.max(Game.date)).scalar()
    dates = db.session.query(Game.date).order_by(Game.date.desc()).limit(constants.TBL_COL)
    # build_plot()
    games = []
    result = []
    for digit in range(1, 25):
        result = get_digit_row(digit, play)
        games.append({'digit': digit, 'game': result})
    return render_template('index.html', title='Stat', max_date=max_date, games=games,
                           url='new_plot.png', count_games=len(result), dates=dates, play=play, balance=balance)


@app.route('/collect_games', methods=['POST'])
def collect_games():
    try:
        offset = timezone(timedelta(hours=3))
        now_day = datetime.datetime.now(offset)
        date = request.values.get('day', now_day.strftime("%d.%m.%Y"))
        refresh_game_stat(date)
    except:
        return jsonify({'data': 'error'})
    return jsonify({'data': 'ok'})


@app.route('/settings')
@login_required
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
        play = request.values.get('play', '1').strip()
        series, cnt = get_digit_info(digit)
        full_series = get_diff_series(series)

        stat = render_template('stat.html', series=series, cnt=cnt, digit=digit, play=play, full_series=full_series)
    except Exception as e:
        return jsonify({'data': 'error'})
    return jsonify({'stat': stat})


@app.route('/charts')
@login_required
def charts():
    return render_template('charts.html')


@app.route('/get_hist', methods=['POST'])
def get_hist():
    try:
        digit = request.values.get('digit').strip()
        dataset = get_count_series(digit)
    except Exception as e:
        raise
    return jsonify({'dataset': dataset})


@app.route('/get_trend', methods=['POST'])
def get_trend():
    try:
        digit = request.values.get('digit').strip()
        dataset = get_all_trend(digit)
    except Exception as e:
        raise
    return jsonify({'dataset': dataset})


@app.route('/create_play', methods=['POST'])
def create_play():
    try:
        user = current_user.id

        digit = request.values.get('digit')
        series = bool(int(request.values.get('play')))
        # series = request.values.get('play')
        win = bool(int(request.values.get('win')))
        bet = request.values.get('bet')
        after = request.values.get('after')
        game_number = db.session.query(db.func.max(PlayGame.game_num)).scalar() or 1
        play = Play(game_time=after, game_digit=digit, game_series=series, game_bet=bet, game_win=win)
        db.session.add(play)
        db.session.flush()
        play_game = PlayGame(user_id=user, game_num=game_number + 1, game_id=play.id)
        db.session.add(play_game)

    except Exception as e:
        raise
    else:
        db.session.commit()
    return render_template('index.html')


@app.route('/history')
@login_required
def history():
    all_bet = request.values.get('all', '0')
    bal = request.values.get('bal', '0')
    user = current_user.id
    if all_bet == '0':
        user_games = db.session.query(Play, PlayGame).filter(Play.id == PlayGame.game_id).order_by(
            Play.game_time.desc()).filter(PlayGame.user_id == user)
    else:
        user_games = db.session.query(Play, PlayGame).filter(Play.id == PlayGame.game_id).order_by(
            Play.game_time.desc()).all()

    if bal == '1':
        result = get_all_balance()
        return render_template('history.html', balance=result, bal=bal, all_bet=all_bet)

    calculate_bets(user)
    return render_template('history.html', result=user_games, balance='', all_bet=all_bet)
