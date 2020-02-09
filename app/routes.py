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
from app.games import Loto
from app.models import User, Play, PlayGame, Profile, Notice
from app import work_with_games as wwg
from app import games

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


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = current_user.id
    game_type = request.args.get('game', constants.G1)
    balance = round(wwg.get_balance(user), 2)
    play = request.args.get('play', '1')
    game_model = constants.GAME_MAP[game_type]['model']
    max_date = db.session.query(db.func.max(game_model.date)).scalar()
    dates = db.session.query(game_model.date).order_by(game_model.date.desc()).limit(constants.RAW_LIMIT)
    # build_plot()
    loto = Loto(game_type=game_type)
    ser_type = constants.RD if play == '1' else constants.GR
    games = loto.get_full_view(ser_type=ser_type, limit=constants.RAW_LIMIT)
    count_games = constants.RAW_LIMIT

    return render_template('index.html', title='Stat', max_date=max_date, games=games,
                           url='new_plot.png', count_games=count_games, dates=dates,
                           play=play, balance=balance, game_type=game_type, row_lim=constants.RAW_LIMIT)


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
        game_type = request.values.get('game_type', constants.G1).strip()
        cnt = wwg.get_max_games(game_type)
        stat = render_template('stat.html', cnt=cnt)
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


@app.route('/charts', methods=['GET'])
@login_required
def charts():
    game_type = request.values.get('game_type', '1').strip()
    loto = Loto(game_type=game_type)
    lim = 0
    full_stat = loto.get_full_stat(limit=lim)
    full_event_stat = loto.get_full_events_stat(limit=lim)
    count_games = wwg.get_max_games(game_type)
    max_ser = loto.get_max_series(full_stat)
    max_event_ser = loto.get_max_series(full_event_stat)
    return render_template('charts.html', full_stat=full_stat, full_event_stat=full_event_stat,
                           cnt=count_games, rng=loto.range, max_ser=max_ser,
                           max_event_ser=max_event_ser, event_rng=loto.events)


@app.route('/get_hist', methods=['POST'])
def get_hist():
    try:
        digit = request.values.get('digit').strip()
        game_type = request.values.get('game_type', '1').strip()
        dataset = wwg.get_dataset_series(digit, game_type)
    except Exception as e:
        raise
    return jsonify({'dataset': dataset})


@app.route('/create_play', methods=['POST'])
def create_play():
    try:
        user = current_user.id

        digit = request.values.get('digit')
        series = bool(int(request.values.get('play')))
        win = bool(int(request.values.get('win')))
        bet = request.values.get('bet')
        after = request.values.get('after')
        game_type = int(request.values.get('game_type', 1))
        game_koef = float(request.values.get('game_koef'))

        game_number = db.session.query(db.func.max(PlayGame.game_num)).scalar() or 1
        play = Play(game_time=after, game_dig=digit, game_series=series, game_bet=bet, game_win=win,
                    game_type=game_type, game_koef=game_koef)
        db.session.add(play)
        db.session.flush()
        play_game = PlayGame(user_id=user, game_num=game_number + 1, game_id=play.id)
        db.session.add(play_game)

    except Exception as e:
        return jsonify({'data': 'Пари НЕ принято'})
    else:
        db.session.commit()
    return jsonify({'data': 'Пари принято'})


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
                play = Play(game_time=after, game_dig=digit, game_series=series, game_bet=bet, game_win=win,
                            game_type=game_type, game_koef=game_koef)
                db.session.add(play)
                db.session.flush()
                play_game = PlayGame(user_id=user, game_num=game_number + 1, game_id=play.id)
                db.session.add(play_game)
        for digit in ser1:
            if digit.isdigit():
                win = 0
                game_number = db.session.query(db.func.max(PlayGame.game_num)).scalar() or 1
                play = Play(game_time=after, game_dig=digit, game_series=series, game_bet=bet, game_win=win,
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


@app.route('/notice')
@login_required
def notice():
    rules = []
    user_id = current_user.id
    notices = Notice.query.filter_by(user_id=user_id).first()
    if notices:
        rules = json.loads(notices.rules)
    return render_template('notices.html', rules=rules)


@app.route('/del_notice', methods=['POST'])
@login_required
def del_notice():
    id_notice_rule: str = request.values.get('id_notice_rule')
    if id_notice_rule.isdigit():
        user_id = current_user.id
        notice = Notice.query.filter_by(user_id=user_id).first()
        if notice:
            rules: list = json.loads(notice.rules)
            rules.pop(int(id_notice_rule))
            notice.rules = json.dumps(rules)
            db.session.add(notice)
            db.session.commit()
    return {}



@app.route('/add_notice', methods=['POST'])
@login_required
def add_notice():
    game_type = request.values.get('game_type')
    game_digit = request.values.get('game_digit', '')
    game_size = request.values.get('game_size')
    game_ser = request.values.get('game_ser', '')
    user_id = current_user.id
    notice = Notice.query.filter_by(user_id=user_id).first()
    new_rule = {'game_type': game_type, 'game_digit': game_digit, 'game_size': game_size, 'game_ser': game_ser}
    if notice:
        rules = json.loads(notice.rules)
        if new_rule not in rules:
            rules.append(new_rule)
            notice.rules = json.dumps(rules)
    else:
        rules = json.dumps([new_rule, ])
        notice = Notice(user_id=user_id, rules=rules)

    db.session.add(notice)
    db.session.commit()
    return {}


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
    game_type = request.values.get('game_type')
    game_digit = request.values.get('game_digit')
    game_ser = request.values.get('game_ser')
    profile = Profile.query.get(id_profile)
    profile.rules = json.dumps(
        {'start': start, 'stop': stop, 'game': cnt_game, 'game_start': game_start,
         'game_type': game_type, 'game_digit': game_digit, 'game_ser': game_ser})
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


@app.route('/get_kf', methods=['POST'])
@login_required
def get_kf():
    return jsonify({k: v['kf'] for k, v in constants.SPEC_MAP.items()})
