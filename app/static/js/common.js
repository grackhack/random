function get_games() {
    $.post('/collect_games', {
                data: 12
            }).done(function(response) {
                location.reload();
                $("#msg").addClass("alert alert-success");
                $("#msg").html("<p> Refresh done!</p>");
            }).fail(function() {
                console.log('fail')
            });

}