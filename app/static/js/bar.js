function hist(digit) {
    $.post('/get_hist', {
        digit: digit,
    }).done(function (response) {
        $("#hw").html(`Серии не выпадений числа: ${digit}. Инфо`);
        $("#hl").html(`Серии выпадений числа: ${digit}. Инфо`);
        show_bar(response.dataset)
    }).fail(function () {
        $("#msg").addClass("alert alert-danger");
        $("#msg").html("<p> Fail!</p>");
    });
}

function show_bar(data) {
    /* chart.js chart examples */

// chart colors
//     var colors = ['#007bff', '#28a745', '#444444', '#ffc107', '#dc3545', '#bf14de'];

    var chBarW = document.getElementById("chBarW");
    var chBarL = document.getElementById("chBarL");

    var chartDataW =  data.W;
    var chartDataL =  data.L;
        // {
        // labels: [2.000e+00, 5.450e+02, 1.088e+03, 1.631e+03, 2.174e+03, 2.717e+03, 3.260e+03, 3.803e+03, 4.346e+03, 4.889e+03, 5.432e+03],
        // datasets: [
        //     {
        //         data: [54, 50, 47, 50, 50, 56, 51, 56, 62, 54,],
        //         backgroundColor: colors[0]
        //     },
            // {
            //     data: [209, 245, 383, 403, 589, 692, 580],
            //     backgroundColor: colors[1]
            // },
            // {
            //     data: [489, 135, 483, 290, 189, 603, 600],
            //     backgroundColor: colors[2]
            // },
            // {
            //     data: [639, 465, 493, 478, 589, 632, 674],
            //     backgroundColor: colors[4]
            // }
    //     ]
    // };

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