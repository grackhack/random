import datetime
import json
from datetime import timezone, timedelta
from random import random
from typing import List

import pandas as pd
from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from app import app
from app import constants
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Play, PlayGame, Profile
from app.work_with_games import refresh_game_stat, get_digit_info, get_diff_series, get_count_series, calculate_bets, \
    get_balance, get_all_balance, get_all_trend
from config import Config
from app.emu_game import emulate, calculate_emu_games


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


def get_digit_row(digit, play, game_type: str):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    connection = engine.raw_connection()
    df = pd.read_sql_query("""
        select de{d:} from (select date,de{d:}  from {tbl_name:} order by date desc limit {tbl:}) a order by date;       
        """.format(d=digit, tbl=constants.TBL_COL, tbl_name=constants.GAME_MAP[game_type]['tbl']), connection)
    df = df.fillna(0)
    row = df.replace(True, 1)[f'de{digit}'].tolist()
    history = get_play_history(row, positive=play)

    return history


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user.id
    game_type = request.args.get('game', '1')
    balance = round(get_balance(user), 2)
    play = request.args.get('play', '1')
    game_model = constants.GAME_MAP[game_type]['model']
    max_date = db.session.query(db.func.max(game_model.date)).scalar()
    dates = db.session.query(game_model.date).order_by(game_model.date.desc()).limit(constants.TBL_COL)
    # build_plot()
    games = []
    result = []
    for digit in constants.GAME_MAP[game_type]['range']:
        result = get_digit_row(digit, play, game_type)
        games.append({'digit': digit, 'game': result})
    return render_template('index.html', title='Stat', max_date=max_date, games=games,
                           url='new_plot.png', count_games=len(result), dates=dates,
                           play=play, balance=balance, game_type=game_type)


@app.route('/collect_games', methods=['POST'])
def collect_games():
    try:
        offset = timezone(timedelta(hours=3))
        now_day = datetime.datetime.now(offset)
        date = request.values.get('day', now_day.strftime("%d.%m.%Y"))
        game_type = request.values.get('game_type', '1')
        refresh_game_stat(date, game_type)
    except Exception as e:
        print(e)
        return jsonify({'data': 'error'})
    return jsonify({'data': 'ok'})


@app.route('/settings')
@login_required
def settings():
    game_type = request.values.get('game_type', '1')
    game_tbl = constants.GAME_MAP[game_type]['tbl']
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    result = engine.execute("""
    select COUNT(*) as count, date_trunc('day', date) as day FROM {tbl:} GROUP BY day ORDER BY day desc
    """.format(tbl=game_tbl))
    rows = result.fetchall()

    return render_template('settings.html', result=rows, game_type=game_type)


@app.route('/get_info', methods=['POST'])
def get_info():
    try:

        digit = request.values.get('digit').strip()
        play = request.values.get('play', '1').strip()
        game_type = request.values.get('game_type', '1').strip()
        series, cnt = get_digit_info(digit, game_type)
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
        game_type = request.values.get('game_type', '1').strip()
        dataset = get_count_series(digit, game_type)
    except Exception as e:
        raise
    return jsonify({'dataset': dataset})


@app.route('/get_trend', methods=['POST'])
def get_trend():
    try:
        digit = request.values.get('digit').strip()
        game_type = request.values.get('game_type', '1').strip()
        dataset = get_all_trend(digit, game_type)
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
        game_type = int(request.values.get('game_type', 1))
        game_koef = float(request.values.get('game_koef'))

        game_number = db.session.query(db.func.max(PlayGame.game_num)).scalar() or 1
        play = Play(game_time=after, game_digit=digit, game_series=series, game_bet=bet, game_win=win,
                    game_type=game_type, game_koef=game_koef)
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
        user_games = db.session.query(Play, PlayGame, User).filter(Play.id == PlayGame.game_id).filter(
            PlayGame.user_id == User.id).order_by(
            Play.game_time.desc()).filter(PlayGame.user_id == user)
    else:
        user_games = db.session.query(Play, PlayGame, User).filter(Play.id == PlayGame.game_id).filter(
            PlayGame.user_id == User.id).order_by(
            Play.game_time.desc()).all()

    if bal == '1':
        result = get_all_balance()
        return render_template('history.html', balance=result, bal=bal, all_bet=all_bet)

    calculate_bets(user)
    return render_template('history.html', result=user_games, balance='', all_bet=all_bet)


@app.route('/emu')
@login_required
def emu():
    profiles = db.session.query(Profile.id, Profile.name).filter(Profile.user_id == User.id).order_by(
        Profile.name).all()
    return render_template('emu.html', profiles=profiles)


@app.route('/add_profile', methods=['POST'])
@login_required
def add_profile():
    rules = json.dumps({})
    skip_time = json.dumps({})
    user_id = current_user.id
    profile_name = request.values.get('pname')
    profile = Profile(user_id=user_id, name=profile_name, rules=rules, skip_time=skip_time)
    db.session.add(profile)
    db.session.commit()
    return {}


@app.route('/add_rule', methods=['POST'])
@login_required
def add_rule():
    id_profile = request.values.get('id_profile')
    start = request.values.get('start')
    stop = request.values.get('stop')
    cnt_game = request.values.get('game')
    game_start = request.values.get('game_start')
    game_type = request.values.get('game_type')
    profile = Profile.query.get(id_profile)
    profile.rules = json.dumps({'start': start, 'stop': stop, 'game': cnt_game,'game_start':game_start, 'game_type': '1'})
    db.session.add(profile)
    db.session.commit()
    return {}


@app.route('/load_rule', methods=['POST'])
@login_required
def load_rule():
    context = {'rules': {}, 'skip_time': {}}
    id_profile = request.values.get('id_profile')
    rule = db.session.query(Profile.rules, Profile.skip_time).filter(Profile.id == id_profile).first()
    if rule:
        rules = json.loads(rule.rules)
        skip_time = json.loads(rule.skip_time)
        context['rules'] = rules
        context['skip_time'] = skip_time
    return context


@app.route('/start_emu', methods=['POST'])
@login_required
def start_emu():
    context = {}
    id_profile = request.values.get('id_profile')
    rule = db.session.query(Profile.rules, Profile.skip_time).filter(Profile.id == id_profile).first()
    if rule:
        rules = json.loads(rule.rules)
        skip_time = json.loads(rule.skip_time)
        stat = emulate(rules)
        info = calculate_emu_games(stat)
        # context['stat'] = stat
        context['info'] = info
    return context
