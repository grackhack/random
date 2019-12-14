function get_games() {
    $.post('/collect_games', {
                data: 12
            }).done(function(response) {
                console.log(response['data'])
            }).fail(function() {
                console.log('fail')
            });

}