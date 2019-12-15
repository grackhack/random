function get_games() {
    $.post('/collect_games', {
                data: 12
            }).done(function(response) {
                location.reload();
                $("#msg").addClass("alert alert-success");
                $("#msg").html("<p> Refresh done!</p>");
            }).fail(function() {
                location.reload();
                $("#msg").addClass("alert alert-danger");
                $("#msg").html("<p> Fail!</p>");
            });

}

function update_by_date(date) {
    $.post('/collect_games', {
                day: date
            }).done(function(response) {
                location.reload();
                $("#msg").addClass("alert alert-success");
                $("#msg").html("<p> Refresh done!</p>");
            }).fail(function() {
                location.reload();
                $("#msg").addClass("alert alert-danger");
                $("#msg").html("<p> Fail!</p>");
            });

}

