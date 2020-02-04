import datetime
import json
from datetime import timezone, timedelta
from random import random
from typing import List, Tuple

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
from app import work_with_games as wwg
# from app.work_with_games import refresh_game_stat, get_digit_info, get_diff_series, get_count_series, calculate_bets, \
#     get_balance, get_all_balance, get_all_trend, get_groups, get_raw_data, get_full_counts

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
    for i in row[::-1]:
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


def get_view_series(digit: int, game_type: str) -> List[int]:
    raw = wwg.get_raw_data(digit, game_type, limit=constants.TBL_COL)
    return list(map(int, raw))


def get_view_kseries(game_type: str) -> List[Tuple[str, List[int]]]:
    all_raw = []

    if game_type == constants.G1:
        raw = []
        raw2 = []
        de1 = wwg.get_raw_data('1', game_type, limit=constants.TBL_COL)
        de2 = wwg.get_raw_data('2', game_type, limit=constants.TBL_COL)
        de3 = wwg.get_raw_data('3', game_type, limit=constants.TBL_COL)
        de4 = wwg.get_raw_data('4', game_type, limit=constants.TBL_COL)
        de5 = wwg.get_raw_data('5', game_type, limit=constants.TBL_COL)
        de6 = wwg.get_raw_data('6', game_type, limit=constants.TBL_COL)
        de7 = wwg.get_raw_data('7', game_type, limit=constants.TBL_COL)
        de8 = wwg.get_raw_data('8', game_type, limit=constants.TBL_COL)
        de9 = wwg.get_raw_data('9', game_type, limit=constants.TBL_COL)
        de10 = wwg.get_raw_data('10', game_type, limit=constants.TBL_COL)
        de11 = wwg.get_raw_data('11', game_type, limit=constants.TBL_COL)
        de12 = wwg.get_raw_data('12', game_type, limit=constants.TBL_COL)
        de13 = wwg.get_raw_data('13', game_type, limit=constants.TBL_COL)
        de14 = wwg.get_raw_data('14', game_type, limit=constants.TBL_COL)
        de15 = wwg.get_raw_data('15', game_type, limit=constants.TBL_COL)
        de16 = wwg.get_raw_data('16', game_type, limit=constants.TBL_COL)
        de17 = wwg.get_raw_data('17', game_type, limit=constants.TBL_COL)
        de18 = wwg.get_raw_data('18', game_type, limit=constants.TBL_COL)
        de19 = wwg.get_raw_data('19', game_type, limit=constants.TBL_COL)
        de20 = wwg.get_raw_data('20', game_type, limit=constants.TBL_COL)
        de21 = wwg.get_raw_data('21', game_type, limit=constants.TBL_COL)
        de22 = wwg.get_raw_data('22', game_type, limit=constants.TBL_COL)
        de23 = wwg.get_raw_data('23', game_type, limit=constants.TBL_COL)
        de24 = wwg.get_raw_data('24', game_type, limit=constants.TBL_COL)
        for i, j, k, l in zip(de5, de10, de15, de20):
            if i == j == k == l == '0':
                raw.append(1)
            else:
                raw.append(0)
        all_raw.append(('k15', raw))

        for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24 in zip(
                de1, de2, de3, de4, de5, de6, de7, de8, de9, de10, de11, de12, de13, de14, de15, de16, de17, de18,
                de19, de20, de21, de22, de23, de24):
            if (sum([int(a2), int(a4), int(a6), int(a8), int(a10), int(a12), int(a14), int(a16), int(a18), int(a20),
                     int(a22), int(a24)]) >

                    sum([int(a1), int(a3), int(a5), int(a7), int(a9), int(a11), int(a13), int(a15), int(a17), int(a19),
                         int(a21), int(a23)])):
                raw2.append(1)
            else:
                raw2.append(0)
        all_raw.append(('Ч>Н', raw2))

    if game_type == constants.G2:
        raw = []
        raw2 = []
        de1 = wwg.get_raw_data('1', game_type, limit=constants.TBL_COL)
        de2 = wwg.get_raw_data('2', game_type, limit=constants.TBL_COL)
        de3 = wwg.get_raw_data('3', game_type, limit=constants.TBL_COL)
        de4 = wwg.get_raw_data('4', game_type, limit=constants.TBL_COL)
        de5 = wwg.get_raw_data('5', game_type, limit=constants.TBL_COL)
        de6 = wwg.get_raw_data('6', game_type, limit=constants.TBL_COL)
        de7 = wwg.get_raw_data('7', game_type, limit=constants.TBL_COL)
        de8 = wwg.get_raw_data('8', game_type, limit=constants.TBL_COL)
        de9 = wwg.get_raw_data('9', game_type, limit=constants.TBL_COL)
        de10 = wwg.get_raw_data('10', game_type, limit=constants.TBL_COL)
        de11 = wwg.get_raw_data('11', game_type, limit=constants.TBL_COL)
        de12 = wwg.get_raw_data('12', game_type, limit=constants.TBL_COL)
        de13 = wwg.get_raw_data('13', game_type, limit=constants.TBL_COL)
        de14 = wwg.get_raw_data('14', game_type, limit=constants.TBL_COL)
        de15 = wwg.get_raw_data('15', game_type, limit=constants.TBL_COL)
        de16 = wwg.get_raw_data('16', game_type, limit=constants.TBL_COL)
        de17 = wwg.get_raw_data('17', game_type, limit=constants.TBL_COL)
        de18 = wwg.get_raw_data('18', game_type, limit=constants.TBL_COL)
        de19 = wwg.get_raw_data('19', game_type, limit=constants.TBL_COL)
        de20 = wwg.get_raw_data('20', game_type, limit=constants.TBL_COL)
        de21 = wwg.get_raw_data('21', game_type, limit=constants.TBL_COL)
        de22 = wwg.get_raw_data('22', game_type, limit=constants.TBL_COL)
        de23 = wwg.get_raw_data('23', game_type, limit=constants.TBL_COL)
        de24 = wwg.get_raw_data('24', game_type, limit=constants.TBL_COL)
        de25 = wwg.get_raw_data('25', game_type, limit=constants.TBL_COL)
        de26 = wwg.get_raw_data('26', game_type, limit=constants.TBL_COL)

        for a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23, a24, a25, a26 in zip(
                de1, de2, de3, de4, de5, de6, de7, de8, de9, de10, de11, de12, de13, de14, de15, de16, de17, de18,
                de19, de20, de21, de22, de23, de24, de25, de26):
            if (a2==a4==a6==a8==a10==a12==a14==a16==a18==a20==a22==a24==a26=='0'):
                raw.append(1)
            else:
                raw.append(0)
            if (a1 == a3 == a5 == a7 == a9 == a11 == a13 == a15 == a17 == a19 == a21 == a23 == a25 == '0'):
                raw2.append(1)
            else:
                raw2.append(0)
        all_raw.append(('Ч13', raw2))
        all_raw.append(('Н13', raw))

    if game_type == constants.G3:
        raw1 = []
        raw2 = []
        de0 = wwg.get_raw_data('0', game_type, limit=constants.TBL_COL)
        de1 = wwg.get_raw_data('1', game_type, limit=constants.TBL_COL)
        de2 = wwg.get_raw_data('2', game_type, limit=constants.TBL_COL)
        de3 = wwg.get_raw_data('3', game_type, limit=constants.TBL_COL)
        de4 = wwg.get_raw_data('4', game_type, limit=constants.TBL_COL)
        de5 = wwg.get_raw_data('5', game_type, limit=constants.TBL_COL)
        de6 = wwg.get_raw_data('6', game_type, limit=constants.TBL_COL)
        de7 = wwg.get_raw_data('7', game_type, limit=constants.TBL_COL)
        de8 = wwg.get_raw_data('8', game_type, limit=constants.TBL_COL)
        de9 = wwg.get_raw_data('9', game_type, limit=constants.TBL_COL)
        for a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 in zip(de0, de1, de2, de3, de4, de5, de6, de7, de8, de9):
            if a1 == a3 == a5 == a7 == a9 == '0':
                raw1.append(1)
            else:
                raw1.append(0)
            if a0 == a2 == a4 == a6 == a8 == '0':
                raw2.append(1)
            else:
                raw2.append(0)
        all_raw.append(('BЧ', raw1))
        all_raw.append(('HЧ', raw2))
    return all_raw


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user.id
    game_type = request.args.get('game', '1')
    balance = round(wwg.get_balance(user), 2)
    play = request.args.get('play', '1')
    game_model = constants.GAME_MAP[game_type]['model']
    max_date = db.session.query(db.func.max(game_model.date)).scalar()
    dates = db.session.query(game_model.date).order_by(game_model.date.desc()).limit(constants.TBL_COL)
    # build_plot()
    games = []
    result = []
    for digit in constants.GAME_MAP[game_type]['range']:
        raw_series = get_view_series(digit, game_type)
        history = get_play_history(raw_series, positive=play)
        games.append({'digit': digit, 'game': history})

    if game_type == constants.G1:
        games.append({'digit': '', 'game': []})
        raw_series = get_view_kseries(game_type)
        for k_name, k_series in raw_series:
            history = get_play_history(k_series, positive=play)
            games.append({'digit': k_name, 'game': history})

    if game_type == constants.G2:
        games.append({'digit': '', 'game': []})
        raw_series = get_view_kseries(game_type)
        for k_name, k_series in raw_series:
            history = get_play_history(k_series, positive=play)
            games.append({'digit': k_name, 'game': history})

    if game_type == constants.G3:
        games.append({'digit': '', 'game': []})
        raw_series = get_view_kseries(game_type)
        for k_name, k_series in raw_series:
            history = get_play_history(k_series, positive=play)
            games.append({'digit': k_name, 'game': history})

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
        oper = request.values.get('oper', '0')
        if oper == '1':
            engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
            tbl_name = constants.GAME_MAP[str(game_type) or constants.G2]['tbl']
            engine.execute("""delete from {tbl:} where date::date between '{dt:} 00:00:00'::date and '{dt:} 23:59:59'::date
                """.format(dt=date, tbl=tbl_name))

        if oper == '0':
            wwg.refresh_game_stat(date, game_type)
    except Exception as e:
        print(e)
        return jsonify({'data': 'error'})
    return jsonify({'data': 'ok'})


@app.route('/settings')
@login_required
def settings():
    game_type = request.values.get('game_type', '1')
    clr = request.values.get('clr')

    game_tbl = constants.GAME_MAP[game_type]['tbl']
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    result = engine.execute("""
    select COUNT(*) as count, date_trunc('day', date) as day FROM {tbl:} GROUP BY day ORDER BY day desc
    """.format(tbl=game_tbl))
    rows = result.fetchall()
    if clr == '1':
        all_bal = wwg.get_all_balance()
        for uname, bal, _, _, _, _ in all_bal:
            engine.execute("""Update "user" set balance={bal:} where username='{uname:}'
            """.format(uname=uname, bal=bal))
        engine.execute("""delete from play_game""")
        engine.execute("""delete from play""")

    return render_template('settings.html', result=rows, game_type=game_type)


@app.route('/get_info', methods=['POST'])
def get_info():
    """Инфо по клику на цифру"""
    try:
        digit = request.values.get('digit').strip()
        play = request.values.get('play', '1').strip()
        game_type = request.values.get('game_type', '1').strip()
        series, cnt = wwg.get_digit_info(digit, game_type)
        full_series = wwg.get_diff_series(series)

        stat = render_template('stat.html', series=series, cnt=cnt, digit=digit, play=play, full_series=full_series)
    except Exception as e:
        return jsonify({'data': 'error'})
    return jsonify({'stat': stat})


@app.route('/find_gr', methods=['POST'])
def find_gr():
    try:
        group = int(request.values.get('group', 0).strip())
        game_type = request.values.get('game_type', '1').strip()
        groups = wwg.get_groups(group, game_type)
        return jsonify({'groups': groups})
    except Exception as e:
        return jsonify({'data': 'error'})


@app.route('/charts')
@login_required
def charts():
    full_stat = wwg.get_full_stat(constants.G1)
    raw = wwg.get_raw_data('1', constants.G1)
    count_games = len(raw)
    return render_template('charts.html', full_stat=full_stat, cnt=count_games)


@app.route('/get_hist', methods=['POST'])
def get_hist():
    try:
        digit = request.values.get('digit').strip()
        game_type = request.values.get('game_type', '1').strip()
        dataset = wwg.get_count_series(digit, game_type)
    except Exception as e:
        raise
    return jsonify({'dataset': dataset})


@app.route('/get_trend', methods=['POST'])
def get_trend():
    try:
        digit = request.values.get('digit').strip()
        game_type = request.values.get('game_type', '1').strip()
        dataset = wwg.get_all_trend(digit, game_type)
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


@app.route('/gr_create_play', methods=['POST'])
def gr_create_play():
    try:
        user = current_user.id
        series = bool(int(request.values.get('play')))
        bet = request.values.get('bet')
        after = request.values.get('after')
        game_type = int(request.values.get('game_type', 1))
        game_koef = float(request.values.get('game_koef'))
        ser0 = request.values.get('ser0', '')
        ser1 = request.values.get('ser1', '')
        ser0 = ser0.split(' : ')
        ser1 = ser1.split(' : ')

        for digit in ser0:
            if digit.isdigit():
                win = 1
                game_number = db.session.query(db.func.max(PlayGame.game_num)).scalar() or 1
                play = Play(game_time=after, game_digit=digit, game_series=series, game_bet=bet, game_win=win,
                            game_type=game_type, game_koef=game_koef)
                db.session.add(play)
                db.session.flush()
                play_game = PlayGame(user_id=user, game_num=game_number + 1, game_id=play.id)
                db.session.add(play_game)
        for digit in ser1:
            if digit.isdigit():
                win = 0
                game_number = db.session.query(db.func.max(PlayGame.game_num)).scalar() or 1
                play = Play(game_time=after, game_digit=digit, game_series=series, game_bet=bet, game_win=win,
                            game_type=game_type, game_koef=game_koef)
                db.session.add(play)
                db.session.flush()
                play_game = PlayGame(user_id=user, game_num=game_number + 1, game_id=play.id)
                db.session.add(play_game)

    except Exception:
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
            Play.game_time.desc()).order_by(User.id).order_by(Play.game_bet.desc()).order_by(
            Play.game_win.desc()).filter(PlayGame.user_id == user)
    else:
        user_games = db.session.query(Play, PlayGame, User).filter(Play.id == PlayGame.game_id).filter(
            PlayGame.user_id == User.id).order_by(Play.game_time.desc()).order_by(User.id).order_by(
            Play.game_bet.desc()).order_by(Play.game_win.desc()).all()

    if bal == '1':
        result = wwg.get_all_balance()
        return render_template('history.html', balance=result, bal=bal, all_bet=all_bet)

    wwg.calculate_bets(user)
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
    # game_type = request.values.get('game_type')
    profile = Profile.query.get(id_profile)
    profile.rules = json.dumps(
        {'start': start, 'stop': stop, 'game': cnt_game, 'game_start': game_start, 'game_type': '1'})
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
        # skip_time = json.loads(rule.skip_time)
        stat = emulate(rules)
        info = calculate_emu_games(stat)
        # context['stat'] = stat
        context['info'] = info
    return context
