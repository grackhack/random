function showTrend(digit, game_type) {
    console.log('asd');
    $.post('/show_trend', {
        digit: digit,
        game_type: game_type
    }).done(function (data) {
        $("#bok").html(data.data);
    })
}