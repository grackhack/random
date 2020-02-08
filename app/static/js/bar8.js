function hist(digit, game_type) {
    $("#bet_digit").text(digit)
    $.post('/get_hist', {
        digit: digit,
        game_type: game_type
    }).done(function (response) {
        // $("#hw").html(`Серии не выпадений числа: ${digit}. Инфо`);
        // $("#hl").html(`Серии выпадений числа: ${digit}. Инфо`);
        show_bar(response.dataset)
        $("#lost_games").html(response.dataset.lost_games);

    }).fail(function () {
        $("#msg").addClass("alert alert-danger");
        $("#msg").html("<p> Fail!</p>");
    });
}

function show_bar(data) {
    /* chart.js chart examples */

    var chBarW = document.getElementById("chBarW");
    var chBarL = document.getElementById("chBarL");

    var chartDataW =  data.W;
    var chartDataL =  data.L;

    if (chBarW) {
        new Chart(chBarW, {
            type: 'bar',
            data: chartDataW,
            options: {
                scales: {
                    xAxes: [{
                        barPercentage: 1,
                        categoryPercentage: 1
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                },
                legend: {
                    display: false
                }
            }
        });
    }
    if (chBarL) {
        new Chart(chBarL, {
            type: 'bar',
            data: chartDataL,
            options: {
                scales: {
                    xAxes: [{
                        barPercentage: 1,
                        categoryPercentage: 1
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                },
                legend: {
                    display: false
                }
            }
        });
    }
}