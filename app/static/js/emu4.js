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
        id_profile: idProfile
    }).done(function (resp) {
        let ruleRow = '';
        for (let [key, val] of Object.entries(resp.rules)) {
            ruleRow += `<div class="col">${key} : ${val}</div>`;
            $(`#e_${key}`).val(val)
        }
        rules.html(ruleRow)
        for (let [key, val] of Object.entries(resp.skip_time)) {
            console.log(key, val)
        }
    })
}

function addRule() {
    let msg = $("#msg");
    let idProfile = $('#profile').val();
    let start = parseInt($("#e_start").val());
    let stop = parseInt($("#e_stop").val());
    let game_start = parseInt($("#e_game_start").val());
    let game = parseInt($("#e_game").val());
    let game_type = parseInt($("#e_game_type").val());
    if (isNaN(start) || isNaN(stop) || isNaN(game)) {
        msg.addClass("alert alert-danger");
        msg.html('Не все поля заполнены!')
        return
    }
    $.post('/add_rule', {
        id_profile: idProfile,
        start: start,
        stop: stop,
        game: game,
        game_start: game_start,
        game_type: game_type,
    }).done(function (response) {
        loadRule()
    })
}

function startEmu() {
    let idProfile = $('#profile').val();
    let info = $('#info');
    let total = $('#total');
    $.post('/start_emu', {
        id_profile: idProfile,
    }).done(function (response) {
        let totalSum = `<div>Итого: ${response.info[1]}</div>`
        let strInfo = ''
        for (let [series, digits] of Object.entries(response.info[0])) {
            strInfo += '<div  class="row justify-content-between">'
            strInfo += `<div class="col">Cерии: ${series}</div>`;
            strInfo += '</div>'
            strInfo += '<div  class="row justify-content-between">'
            for (let [key, val] of Object.entries(digits)) {
                strInfo += `<div class="col"><b>${key}</b><br>${val}</div>`;
                $(`#e_${key}`).val(val)
            }
            strInfo += '</div>'
        }
        info.html(strInfo)
        total.html(totalSum)

    })
}