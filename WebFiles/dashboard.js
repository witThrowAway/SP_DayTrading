
(function () {
  'use strict'

  feather.replace()


  var ctx = document.getElementById('myChart')

  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        '8AM',
        '9AM',
        '10AM',
        '11AM',
        '12PM',
        '1PM',
        '2PM'
      ],
      datasets: [{
        data: [],

        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
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
  })
}())
