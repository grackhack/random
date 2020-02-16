KF = {
    '1': {1: 1.92, 0: 1.92},
    '2': {1: 5.75, 0: 1.14},
    '3': {1: 3.45, 0: 1.33},
    '4': {1: 2.38, 0: 1.61},
    '41': {1: 1.75, 0: 2.13},
    '5': {1: 2.38, 0: 1.61},
    '51': {1: 1.75, 0: 2.13},


    'K15': {1: 15.0, 0: 1.03},
    'E>O': {1: 2.84, 0: 1.45},
    'NR': {1: 2.17, 0: 1.72},
    'EVEN': {1: 6.75, 0: 1.12},
    'ODD': {1: 6.75, 0: 1.12},
    'EQ': {1: 3.33, 0: 1.35},
    'MNE': {1: 2.80, 0: 1.46},
    'MNE1': {1: 2.88, 0: 1.44},
    'MNE2': {1: 2.88, 0: 1.44},
    'MXE': {1: 1.46, 0: 2.80},
    'MXE1': {1: 1.56, 0: 2.50},
    'MXE2': {1: 1.56, 0: 2.50},
    'K152': {1: 2.16, 0: 1.73},
    'K148': {1: 1.81, 0: 2.04},
    '1K84': {1: 1.72, 0: 2.17},
    '2K84': {1: 1.72, 0: 2.17},
    '1K88': {1: 2.17, 0: 1.72},
    '2K88': {1: 2.17, 0: 1.72},
    'M2_5': {1: 2.72, 0: 1.48},
    'M1_5': {1: 1.85, 0: 2.00},
    '1M1_5': {1: 2.13, 0: 1.75},
    '1M2_5': {1: 5.15, 0: 1.18},
    '2M1_5': {1: 2.13, 0: 1.75},
    '2M2_5': {1: 5.15, 0: 1.18},
    'S14': {1: 2.24, 0: 1.68},
    'S12': {1: 1.68, 0: 2.24},
    'DNR': {1: 2.50, 0: 1.56},
    'DEB': {1: 3.05, 0: 1.40},
    '---': {1: 1.00, 0: 1.00},

};


function showMsg(msgType, msgText) {
    msg = $("#msg");
    msg.addClass(`alert alert-${msgType}`);
    msg.html(msgText);
    setTimeout(function () {
        msg.removeClass(`alert alert-${msgType}`);
        msg.html('');
    }, 3000);
}

function showErrMsg(msgText) {
    let msg = $("#err_msg");
    msg.addClass('alert alert-danger');
    msg.html(msgText);
    setTimeout(function () {
        msg.removeClass('alert alert-danger');
        msg.html('');
    }, 3000);
}


function get_games(game_type) {
    $.post('/collect_games', {
        game_type: game_type
    }).done(function () {
        location.reload();
        showMsg('success', 'Refresh done!')
    }).fail(function () {
        location.reload();
        showMsg('danger', 'Fail!')
    });
}

function update_by_date(date, game_type, oper) {
    $.post('/collect_games', {
        day: date,
        game_type: game_type,
        oper: oper
    }).done(function () {
        location.reload();
        showMsg('success', 'Refresh done!')
    }).fail(function () {
        location.reload();
        showMsg('danger', 'Fail!')
    });
}


function get_info(digit, play, game_type) {
    $("#bet_digit").text(digit);
    // if (isNaN(parseInt(digit))) {
    //     return
    // }
    $.post('/get_info', {
        digit: digit,
        play: play,
        game_type: game_type
    }).done(function (response) {
        $('#stat').html(response.stat)
    }).fail(function () {
        showMsg('danger', 'Fail')
    });
    hist(digit, game_type)
}

function find_gr(group, game_type) {
    $.post('/find_gr', {
        group: group,
        game_type: game_type
    }).done(function (response) {
        let cnt = 0;
        for (let [series, digits] of Object.entries(response.groups)) {
            $(`#gr_${series}`).html(digits.join(' : '));
            cnt += digits.length
        }
        $('#gr_bet_win').val(cnt)
    }).fail(function () {
        showErrMsg('Fail')
    });

}

function ins_bet(count) {
    $("#bet_count").val(count);
    refresh_bet_sum()
}

function gr_ins_bet(count) {
    $("#gr_bet_count").val(count);
    refresh_gr_bet_sum()
}

function ins_gr(count, game_type) {
    $("#gr_series").val(count);
    find_gr(count, game_type);
    refresh_gr_bet_sum()
}


function ins_win(win) {
    let betDigit = $("#bet_digit").text().trim();
    let betGameType = $("#bet_game_type").val();
    if (win === 0) {
        $("#bet_win").val('Не выпадет');
    } else {
        $("#bet_win").val('Выпадет');
    }

    if (!$.isNumeric(betDigit)) {
        $("#bet_k").text(KF[betDigit][win]);
    } else {
        if ((betGameType === '4' || betGameType === '5') && (betDigit === '1' || betDigit === '2' || betDigit === '3' || betDigit === '4')) {
            $("#bet_k").text(KF[`${betGameType}1`][win]);
        } else {
            $("#bet_k").text(KF[betGameType][win]);
        }
    }

    refresh_bet_sum()
}

function refresh_bet_sum() {
    let betCount = parseInt($("#bet_count").val());
    let betK = parseFloat($("#bet_k").text().trim());
    $("#bet_sum").text((betCount * betK).toFixed(2));
}

function refresh_gr_bet_sum() {
    let betCount = parseInt($("#gr_bet_count").val());
    parseFloat($("#gr_bet_k").text().trim());
    let cnt = parseInt($("#gr_bet_win").val());
    $("#gr_bet_sum").text((betCount * cnt).toFixed(2));
}

function bet() {
    let betDigit = $("#bet_digit").text().trim();
    let betCount = parseInt($("#bet_count").val());
    let betWin = $("#bet_win").val();
    let betSeries = $("#bet_series").val();
    let betGameType = $("#bet_game_type").val();
    let betAfter = $("#bet_after").text().trim();
    let balance = parseFloat($("#bal").text().trim());
    let betKoef = $("#bet_k").text().trim();

    if (isNaN(betCount)) {
        showErrMsg('Не выбрана ставка');
        return
    }

    if (betDigit === '?') {
        showErrMsg('Не выбрано число');
        return
    }

    if (betWin === 'Выпадет') {
        betWin = 1
    }

    if (betWin === 'Не выпадет') {
        betWin = 0
    }

    if ([0, 1].indexOf(betWin) < 0) {
        showErrMsg('Не выбран тип ставки');
        return
    }
    if ((balance - betCount) < 0) {
        showErrMsg('Нет денег на балансе для ставки');
        return
    }
    $.post('/create_play', {
        digit: betDigit,
        play: betSeries,
        win: betWin,
        bet: betCount,
        after: betAfter,
        game_type: betGameType,
        game_koef: betKoef
    }).done(function () {
        $("#exampleModal").modal('hide');
        showMsg('success', 'Ставка принята!')
    }).fail(function () {
        showErrMsg('Fail');
    });
}

function gr_bet() {
    let grCount = parseInt($("#gr_bet_count").val());
    let grKoef = $("#gr_bet_k").text().trim();
    let grSeries = $("#gr_series").val();
    let ser0 = $("#gr_0").text();
    let ser1 = $("#gr_1").text();
    let grAfter = $("#bet_after").text().trim();
    let grGameType = $("#gr_bet_game_type").val();

    if (isNaN(grSeries)) {
        showErrMsg('Не выбрана серия');
        return
    }
    if (isNaN(grCount)) {
        showErrMsg('Не выбрана ставка');
        return
    }

    $.post('/gr_create_play', {
        play: grSeries,
        bet: grCount,
        after: grAfter,
        game_type: grGameType,
        game_koef: grKoef,
        ser0: ser0,
        ser1: ser1,
    }).done(function () {
        showMsg('success', 'Ставки сделаны!');
        $("#grModal").modal('hide')
    }).fail(function () {
        showErrMsg('Fail');
        $("#grModal").modal('hide')
    });
}


