function add_profile() {
    let profileName = $("#profile_name").val();
    let msg = $("#msg");
    let errmsg = $("#err_msg");
    $.post('/add_profile', {
        pname: profileName
    }).done(function (response) {
        $("#addProfile").modal('hide');
        msg.addClass("alert alert-success");
        msg.html("<p> Профиль создан !</p>");
    }).fail(function () {
        errmsg.addClass("alert alert-danger");
        errmsg.html("<p> Fail!</p>");
    });
}

function loadRule() {
    let idProfile = $('#profile').val();
    let rules = $('#rules');
    let skip_times = $('#skip_times');
    $.post('/load_rule', {
        profile_id: idProfile
    }).done(function (resp) {
        console.log(resp['rules']);

        console.log(resp['skip_time'])

    }).done(function (response) {
        msg.addClass("alert alert-success");
        msg.html("<p> Правило добавлено!</p>");
    })
}

function addRule() {
    let msg = $("#msg");
    let idProfile = $('#profile').val();
    let start = parseInt($("#e_start").val());
    let stop = parseInt($("#e_stop").val());
    if (isNaN(start) || isNaN(stop)) {
        msg.addClass("alert alert-danger");
        msg.html('Не Заполнены поля')
        return
    }
    $.post('/add_rule', {
        id_profile: idProfile,
        start: start,
        stop: stop
    })
}