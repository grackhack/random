const RANGE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

function clear_msg() {
    $("#msg").removeClass("alert alert-success");
    $("#msg").html('');
}

function get_games() {
    clear_msg()
    $.post('/collect_games', {
        data: 12
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

function update_by_date(date) {
    clear_msg()
    $.post('/collect_games', {
        day: date
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

function get_info(digit, play) {
    clear_msg()
    $.post('/get_info', {
        digit: digit,
        play: play
    }).done(function (response) {
        $('#stat').html(response.stat)
    }).fail(function () {
        $("#msg").addClass("alert alert-danger");
        $("#msg").html("<p> Fail!</p>");
    });
    hist(digit)
}

function refresh_bet_sum() {
    var betCount = parseInt($("#bet_count").val());
    var betK = parseFloat($("#bet_k").text().trim());
    $("#bet_sum").text((betCount * betK).toFixed(2));
}

function bet() {
    $("#err_msg").removeClass("alert alert-danger");
    $("#err_msg").html('');

    var betDigit = parseInt($("#bet_digit").text().trim());
    var betCount = parseInt($("#bet_count").val());
    var betWin = $("#bet_win").val();
    var betSeries = $("#bet_series").val();
    var betAfter = $("#bet_after").text().trim();
    if (isNaN(betDigit)) {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html('Не выбрано число');
        return
    }
    if (isNaN(betCount)) {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html('Не выбрана ставка')
        return
    }
    if (["0", "1"].indexOf(betWin) < 0) {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html('Не выбран тип ставки')
        return
    }
    $.post('/create_play', {
        digit: betDigit,
        play: betSeries,
        win: betWin,
        bet: betCount,
        after : betAfter,
    }).done(function (response) {
        $("#exampleModal").modal('hide')
        $("#msg").addClass("alert alert-success");
        $("#msg").html("<p> Ставка принята!</p>");
    }).fail(function () {
        $("#err_msg").addClass("alert alert-danger");
        $("#err_msg").html("<p> Fail!</p>");
    });



}


