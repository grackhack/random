function get_games() {
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
    $.post('/get_info', {
        digit: digit,
        play: play
    }).done(function (response) {
        // $('[id^="r"]').popover('dispose');
        // var p = $(`#r${digit}`);
        // p.popover({
        //     html: true,
        //     content: response.stat,
        //     delay: { "show": 500, "hide": 100 }
        //
        // }).popover('show')
        $('#stat').html(response.stat)
    }).fail(function () {
        $("#msg").addClass("alert alert-danger");
        $("#msg").html("<p> Fail!</p>");
    });
}


