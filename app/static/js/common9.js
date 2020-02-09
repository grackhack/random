KF = {
    '1': {1: 1.92, 0: 1.92},
    '2': {1: 5.75, 0: 1.14},
    '3': {1: 3.45, 0: 1.33},

    'k15': {1: 15.0, 0: 1.03},
    'E>O': {1: 2.84, 0: 1.45},
    'NR': {1: 2.17, 0: 1.72},
    'EVEN': {1: 6.75, 0: 1.12},
    'ODD': {1: 6.75, 0: 1.12},
    'E13': {1: 2.84, 0: 1.45},
    'O13': {1: 2.84, 0: 1.45},
    'EQ': {1: 3.33, 0: 1.35},
    'MNE': {1: 2.80, 0: 1.46},
    'MXE': {1: 1.46, 0: 2.80},
    'k152': {1: 2.16, 0: 1.73},
};



function clear_msg() {
    $("#msg").removeClass("alert alert-success");
    $("#msg").html('');
}

function get_games(game_type) {
    clear_msg();
    $.post('/collect_games', {
        game_type: game_type
    }).done(function (response) {
        location.reload();
        $("#msg").addClass("alert alert-success");
        $("#msg").html("<p> Refresh done!</p>");
    }).fail(function () {
        location.reload();
        $("#msg").addClass("alert alert-danger");
        $("#msg").html("<p> Fail!</p>");
    });
}

function update_by_date(date, game_type, oper) {
    clear_msg()
    $.post('/collect_games', {
        day: date,
        game_type: game_type,
        oper: oper
    }).done(function (response) {
        location.reload();
        $("#msg").addClass("alert alert-success");
        $("#msg").html("<p> Refresh done!</p>");
    }).fail(function () {
        location.reload();
        $("#msg").addClass("alert alert-danger");
        $("#msg").html("<p> Fail!</p>");
    });
}


function get_info(digit, play, game_type) {
    clear_msg()
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
        $("#msg").addClass("alert alert-danger");
        $("#msg").html("<p> Fail!</p>");
    });
    hist(digit, game_type)
}

function find_gr(group, game_type) {
    $.post('/find_gr', {
        group: group,
        game_type: game_type
    }).done(function (response) {
        let cnt = 0
        for (let [series, digits] of Object.entries(response.groups)) {
            $(`#gr_${series}`).html(digits.join(' : '))
            cnt += digits.length
        }
        $('#gr_bet_win').val(cnt)
    }).fail(function () {
        $("#msg").addClass("alert alert-danger");
        $("#msg").html("<p> Fail!</p>");
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
    find_gr(count, game_type)
    refresh_gr_bet_sum()
}


function ins_win(win) {
    let betDigit = $("#bet_digit").text().trim();
    let betGameType = $("#bet_game_type").val();
    if (win == 0) {
        $("#bet_win").val('Не выпадет');
    } else {
        $("#bet_win").val('Выпадет');
    }

    if (!$.isNumeric(betDigit)) {
        $("#bet_k").text(KF[betDigit][win]);
    }
    else {
        $("#bet_k").text(KF[betGameType][win]);
    }

    refresh_bet_sum()
}

function refresh_bet_sum() {
    var betCount = parseInt($("#bet_count").val());
    var betK = parseFloat($("#bet_k").text().trim());
    $("#bet_sum").text((betCount * betK).toFixed(2));
}

function refresh_gr_bet_sum() {
    var betCount = parseInt($("#gr_bet_count").val());
    var betK = parseFloat($("#gr_bet_k").text().trim());
    var cnt = parseInt($("#gr_bet_win").val());
    $("#gr_bet_sum").text((betCount * cnt).toFixed(2));
}

function bet() {
    $("#err_msg").removeClass("alert alert-danger");
    $("#err_msg").html('');

    var betDigit = $("#bet_digit").text().trim();
    var betCount = parseInt($("#bet_count").val());
    var betWin = $("#bet_win").val();
    var betSeries = $("#bet_series").val();
    var betGameType = $("#bet_game_type").val();
    var betAfter = $("#bet_after").text().trim();
    var balance = parseFloat($("#bal").text().trim())
    var betKoef = $("#bet_k").text().trim()

    if (isNaN(betCount)) {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html('Не выбрана ставка')
        return
    }
    if (betWin === 'Выпадет') {
        betWin = 1
    }

    if (betWin === 'Не выпадет') {
        betWin = 0
    }

    if ([0, 1].indexOf(betWin) < 0) {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html('Не выбран тип ставки')
        return
    }
    if ((balance - betCount) < 0) {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html('Нет денег на балансе для ставки')
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
    }).done(function (response) {
        $("#exampleModal").modal('hide')
        $("#msg").addClass("alert alert-success");
        $("#msg").html("<p> Ставка принята!</p>");
    }).fail(function () {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html("<p> Fail!</p>");
    });
}

function gr_bet() {
    $("#err_msg").removeClass("alert alert-danger");
    $("#err_msg").html('');

    let grCount = parseInt($("#gr_bet_count").val());
    let grKoef = $("#gr_bet_k").text().trim();
    let grSeries = $("#gr_series").val();
    let ser0 = $("#gr_0").text();
    let ser1 = $("#gr_1").text();
    let grAfter = $("#bet_after").text().trim();
    let grGameType = $("#gr_bet_game_type").val();

    if (isNaN(grSeries)) {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html('Не выбрана серия');
        return
    }
    if (isNaN(grCount)) {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html('Не выбрана ставка')
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
    }).done(function (response) {
        $("#grModal").modal('hide')
        $("#msg").addClass("alert alert-success");
        $("#msg").html("<p> Ставки сделаны!</p>");
    }).fail(function () {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html("<p> Fail!</p>");
    });
}


