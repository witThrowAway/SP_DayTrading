import { websocketClient } from "polygon.io";

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

function getGraphData() {

const stocksWS = websocketClient("PKVAPQS1G0L00QDLGCZR").getStocksWebsocket();

stocksWs.on("message", raw => {
  const message = JSON.parse(raw);
  console.log(message)
  switch (message.ev) {
    case "T":
      // your trade message handler
      console.log(message.ev)
      break;
  }
});

stocksWS.send({ action: "subscribe", params: "T.MSFT" });


}