

function addNotice() {
    let msg = $("#msg");
    let game_type = parseInt($("#n_game_type").val());
    let game_digit = $("#n_game_digit").val();
    let game_size = $("#n_game_size").val();
    let game_ser = $("#n_game_ser").val();

    if (isNaN(game_size)  || isNaN(game_type)) {
        msg.addClass("alert alert-danger");
        msg.html('Не все поля заполнены!')
        return 0
    }
    $.post('/add_notice', {
        game_type: game_type,
        game_digit: game_digit,
        game_size: game_size,
        game_ser: game_ser,
    }).done(function (response) {
        location.reload();
    })
}


function delNotice(idNoticeRule) {
    let idNoticeRow = $(`#id_notice_${idNoticeRule}`)
    $.post('/del_notice', {
        id_notice_rule: idNoticeRule,
    }).done(function (response) {
        idNoticeRow.remove();
        // loadRule()
    })


}