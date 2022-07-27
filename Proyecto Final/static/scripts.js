window.Apex = {
  chart: {
    foreColor: '#fff',
    toolbar: {
      show: false
    },
  },
  colors: ['#FCCF31', '#17ead9', '#f02fc2'],
  stroke: {
    width: 3
  },
  dataLabels: {
    enabled: false
  },
  grid: {
    borderColor: "#40475D",
  },
  xaxis: {
    axisTicks: {
      color: '#333'
    },
    axisBorder: {
      color: "#333"
    }
  },
  fill: {
    type: 'gradient',
    gradient: {
      gradientToColors: ['#F55555', '#6078ea', '#6094ea']
    },
  },
  tooltip: {
    theme: 'dark',
    x: {
      formatter: function (val) {
        return moment(new Date(val)).format("HH:mm:ss")
      }
    }
  },
  yaxis: {
    decimalsInFloat: 2,
    opposite: true,
    labels: {
      offsetX: -10
    }
  }
};



var trigoStrength = 3
var iteration = 11

function getRandom() {
  var i = iteration;
  return (Math.sin(i / trigoStrength) * (i / trigoStrength) + i / trigoStrength + 1) * (trigoStrength * 2)
}

function getRangeRandom(yrange) {
  return Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min
}

function generateMinuteWiseTimeSeries(baseval, count, yrange) {
  var i = 0;
  var series = [];



  while (i < count) {
    var x = baseval;
    var y = ((Math.sin(i / trigoStrength) * (i / trigoStrength) + i / trigoStrength + 1) * (trigoStrength * 2))

    series.push([x, 0]);
    baseval += 1;
    i++;
  }
  return series;
}



function getNewData(baseval, yrange) {
  var newTime = baseval + 300000;
  return {
    x: newTime,
    y: Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min
  }
}


var optionsColumn = {
  series: [{
    name: 'Temperatura',
    data: [0, 0, 0, 0, 0]
  }],
    chart: {
    height: 350,
    type: 'bar',
  },
  plotOptions: {
    bar: {
      borderRadius: 10,
      dataLabels: {
        position: 'top', // top, center, bottom
      },
    }
  },
  dataLabels: {
    enabled: true,
    formatter: function (val) {
      return val + "°";
    },
    offsetY: -20,
    style: {
      fontSize: '12px',
      colors: ["#304758"]
    }
  },

  xaxis: {
    categories: ["S1", "S2", "S3", "S4", "S5"],
    position: 'top',
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    },
    crosshairs: {
      fill: {
        type: 'gradient',
        gradient: {
          colorFrom: '#D8E3F0',
          colorTo: '#BED1E6',
          stops: [0, 100],
          opacityFrom: 0.4,
          opacityTo: 0.5,
        }
      }
    },
    tooltip: {
      enabled: true,
    }
  },
  yaxis: {
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false,
    },
    labels: {
      show: false,
      formatter: function (val) {
        return val + "°";
      }
    }

  },
  title: {
    text: 'Temperaturas',
    floating: true,
    offsetY: 330,
    align: 'center',
    style: {
      color: '#444'
    }
  }
};



var chartColumn = new ApexCharts(
  document.querySelector("#columnchart"),
  optionsColumn
);
chartColumn.render()



var arregloTempSem1 = []
var arregloTempSem2 = []
var arregloTempSem3 = []
var arregloTempSem4 = []
var arregloTempSem5 = []

var seriesS1 = [];
var seriesS2 = [];
var seriesS3 = [];
var seriesS4 = [];
var seriesS5 = [];

var con = 0
        
for(s1 of arregloTempSem1){
  seriesS1.push([con, s1]);
  con+=1
}
con = 0
for(s2 of arregloTempSem2){
  seriesS2.push([con, s2]);
  con+=1
}
con = 0
for(s3 of arregloTempSem3){
  seriesS3.push([con, s3]);
  con+=1
}
con = 0
for(s4 of arregloTempSem4){
  seriesS4.push([con, s4]);
  con+=1
}
con = 0
for(s5 of arregloTempSem5){
  seriesS5.push([con, s5]);
  con+=1
}

var optionsLine = {
  chart: {
    height: 350,
    type: 'line',
    stacked: true,
    animations: {
      enabled: true,
      easing: 'linear',
      dynamicAnimation: {
        speed: 1000
      }
    },
    dropShadow: {
      enabled: true,
      opacity: 0.3,
      blur: 5,
      left: -7,
      top: 22
    },
    events: {
      animationEnd: function (chartCtx, opts) {
                // check animation end event for just 1 series to avoid multiple updates
        if (opts.el.node.getAttribute('index') === '0') {
          window.setTimeout(function () {
            chartCtx.updateOptions({
              series: [{
                data: seriesS1
              }, {
                data: seriesS2
              }, {
                data: seriesS3
              }, {
                data: seriesS4
              }, {
                data: seriesS5
              }],
              subtitle: {
                text: parseInt(getRandom() * Math.random()).toString(),
              }
            }, false, false)
          }, 300)
        }

      }
    },
    toolbar: {
      show: false
    },
    zoom: {
      enabled: false
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'straight',
    width: 5,
  },
  grid: {
    padding: {
      left: 0,
      right: 0
    }
  },
  markers: {
    size: 0,
    hover: {
      size: 0
    }
  },
  series: [{
    name: 'Temperatura Sem. 1',
    data: seriesS5
  }, {
    name: 'Temperatura Sem. 2',
    data: seriesS2
  }, {
    name: 'Temperatura Sem. 3',
    data: seriesS3
  }, {
    name: 'Temperatura Sem. 4',
    data: seriesS4
  }, {
    name: 'Temperatura Sem. 5',
    data: seriesS5
  }],
  xaxis: {
    type: 'numeric',
    range: 20
  },
  title: {
    text: 'Historico de temperaturas',
    align: 'left',
    style: {
      fontSize: '12px'
    }
  },
  subtitle: {
    text: '20',
    floating: true,
    align: 'right',
    offsetY: 0,
    style: {
      fontSize: '22px'
    }
  },
  legend: {
    show: true,
    floating: true,
    horizontalAlign: 'left',
    onItemClick: {
      toggleDataSeries: false
    },
    position: 'top',
    offsetY: -28,
    offsetX: 60
  },
}

var chartLine = new ApexCharts(
  document.querySelector("#linechart"),
  optionsLine
);
chartLine.render()

var optionsProgress1 = {
  chart: {
    height: 70,
    type: 'bar',
    stacked: true,
    sparkline: {
      enabled: true
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: '20%',
      colors: {
        backgroundBarColors: ['#40475D']
      }
    },
  },
  stroke: {
    width: 0,
  },
  series: [{
    name: 'SEMAFORO 1',
    data: [0]
  }],
  title: {
    floating: true,
    offsetX: -10,
    offsetY: 5,
    text: 'SEMAFORO 1'
  },
  subtitle: {
    floating: true,
    align: 'right',
    offsetY: 0,
    text: '0%',
    style: {
      fontSize: '20px'
    }
  },
  tooltip: {
    enabled: false
  },
  xaxis: {
    categories: ['SEMAFORO 1'],
  },
  yaxis: {
    max: 100
  },
  fill: {
    opacity: 1
  }
}

var chartProgress1 = new ApexCharts(document.querySelector('#semaforo1'), optionsProgress1);
chartProgress1.render();


var optionsProgress2 = {
  chart: {
    height: 70,
    type: 'bar',
    stacked: true,
    sparkline: {
      enabled: true
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: '20%',
      colors: {
        backgroundBarColors: ['#40475D']
      }
    },
  },
  colors: ['#17ead9'],
  stroke: {
    width: 0,
  },
  series: [{
    name: 'SEMAFORO 2',
    data: [0]
  }],
  title: {
    floating: true,
    offsetX: -10,
    offsetY: 5,
    text: 'SEMAFORO 2'
  },
  subtitle: {
    floating: true,
    align: 'right',
    offsetY: 0,
    text: '0%',
    style: {
      fontSize: '20px'
    }
  },
  tooltip: {
    enabled: false
  },
  xaxis: {
    categories: ['SEMAFORO 2'],
  },
  yaxis: {
    max: 100
  },
  fill: {
    type: 'gradient',
    gradient: {
      inverseColors: false,
      gradientToColors: ['#6078ea']
    }
  },
}

var chartProgress2 = new ApexCharts(document.querySelector('#semaforo2'), optionsProgress2);
chartProgress2.render();


var optionsProgress3 = {
  chart: {
    height: 70,
    type: 'bar',
    stacked: true,
    sparkline: {
      enabled: true
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: '20%',
      colors: {
        backgroundBarColors: ['#40475D']
      }
    },
  },
  colors: ['#f02fc2'],
  stroke: {
    width: 0,
  },
  series: [{
    name: 'SEMAFORO 3',
    data: [0]
  }],
  fill: {
    type: 'gradient',
    gradient: {
      gradientToColors: ['#6094ea']
    }
  },
  title: {
    floating: true,
    offsetX: -10,
    offsetY: 5,
    text: 'SEMAFORO 3'
  },
  subtitle: {
    floating: true,
    align: 'right',
    offsetY: 0,
    text: '0%',
    style: {
      fontSize: '20px'
    }
  },
  tooltip: {
    enabled: false
  },
  xaxis: {
    categories: ['SEMAFORO 3'],
  },
  yaxis: {
    max: 100
  },
}

var chartProgress3 = new ApexCharts(document.querySelector('#semaforo3'), optionsProgress3);
chartProgress3.render();

var optionsProgress4 = {
  chart: {
    height: 70,
    type: 'bar',
    stacked: true,
    sparkline: {
      enabled: true
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: '20%',
      colors: {
        backgroundBarColors: ['#40475D']
      }
    },
  },
  colors: ['#f02fc2'],
  stroke: {
    width: 0,
  },
  series: [{
    name: 'SEMAFORO 4',
    data: [0]
  }],
  fill: {
    type: 'gradient',
    gradient: {
      gradientToColors: ['#6094ea']
    }
  },
  title: {
    floating: true,
    offsetX: -10,
    offsetY: 5,
    text: 'SEMAFORO 4'
  },
  subtitle: {
    floating: true,
    align: 'right',
    offsetY: 0,
    text: '0%',
    style: {
      fontSize: '20px'
    }
  },
  tooltip: {
    enabled: false
  },
  xaxis: {
    categories: ['SEMAFORO 4'],
  },
  yaxis: {
    max: 100
  },
}

var chartProgress4 = new ApexCharts(document.querySelector('#semaforo4'), optionsProgress4);
chartProgress4.render();

var optionsProgress5 = {
  chart: {
    height: 70,
    type: 'bar',
    stacked: true,
    sparkline: {
      enabled: true
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: '20%',
      colors: {
        backgroundBarColors: ['#40475D']
      }
    },
  },
  colors: ['#f02fc2'],
  stroke: {
    width: 0,
  },
  series: [{
    name: 'SEMAFORO 5',
    data: [0]
  }],
  fill: {
    type: 'gradient',
    gradient: {
      gradientToColors: ['#6094ea']
    }
  },
  title: {
    floating: true,
    offsetX: -10,
    offsetY: 5,
    text: 'SEMAFORO 5'
  },
  subtitle: {
    floating: true,
    align: 'right',
    offsetY: 0,
    text: '0%',
    style: {
      fontSize: '20px'
    }
  },
  tooltip: {
    enabled: false
  },
  xaxis: {
    categories: ['SEMAFORO 5'],
  },
  yaxis: {
    max: 100
  },
}

var chartProgress5 = new ApexCharts(document.querySelector('#semaforo5'), optionsProgress5);
chartProgress5.render();

var ajaxFUN = function () {
  $.ajax({
    url: '/determinarActualizacion',
    dataType: 'json',
    success: function (data) {
      aux = data["NOTIFICACION_AUTOS"];
      if(aux != {} && aux != undefined){
        if(aux["actualizar"] == "SI"){
          var semaforo1Data = aux["cantidadAutosSemaforo1"];
          chartProgress1.updateOptions({
            series: [{
              data: [100-(semaforo1Data/5)*100]
            }],
            subtitle: {
              text: 100-(semaforo1Data/5)*100 + "%"
            }
          })

          var semaforo2Data = aux["cantidadAutosSemaforo2"];
          chartProgress2.updateOptions({
            series: [{
              data: [100-(semaforo2Data/5)*100]
            }],
            subtitle: {
              text: 100-(semaforo2Data/5)*100 + "%"
            }
          })

          var semaforo3Data = aux["cantidadAutosSemaforo3"];
          chartProgress3.updateOptions({
            series: [{
              data: [100-(semaforo3Data/5)*100]
            }],
            subtitle: {
              text: 100-(semaforo3Data/5)*100 + "%"
            }
          })

          var semaforo4Data = aux["cantidadAutosSemaforo4"];
          chartProgress4.updateOptions({
            series: [{
              data: [100-(semaforo4Data/5)*100]
            }],
            subtitle: {
              text: 100-(semaforo4Data/5)*100 + "%"
            }
          })

          var semaforo5Data = aux["cantidadAutosSemaforo5"];
          chartProgress5.updateOptions({
            series: [{
              data: [100-(semaforo5Data/5)*100]
            }],
            subtitle: {
              text: 100-(semaforo5Data/5)*100 + "%"
            }
          })


        }
      }      


          

      auxTemp = data["NOTIFICACION_TEMPERATURA"];
      if(auxTemp != {} && auxTemp != undefined){
        if(auxTemp["actualizar"] == "SI"){
          var tempSem1Data = auxTemp["temperaturaSemaforo1"];
          var tempSem2Data = auxTemp["temperaturaSemaforo2"];
          var tempSem3Data = auxTemp["temperaturaSemaforo3"];
          var tempSem4Data = auxTemp["temperaturaSemaforo4"];
          var tempSem5Data = auxTemp["temperaturaSemaforo5"];
          
          if(arregloTempSem1[arregloTempSem1.length-1] != tempSem1Data){
            arregloTempSem1.push(tempSem1Data)
          }
          if(arregloTempSem2[arregloTempSem2.length-1] != tempSem2Data){
            arregloTempSem2.push(tempSem2Data)
          }
          if(arregloTempSem3[arregloTempSem3.length-1] != tempSem3Data){
            arregloTempSem3.push(tempSem3Data)
          }
          if(arregloTempSem4[arregloTempSem4.length-1] != tempSem4Data){
            arregloTempSem4.push(tempSem4Data)
          }
          if(arregloTempSem5[arregloTempSem5.length-1] != tempSem5Data){
            arregloTempSem5.push(tempSem5Data)
          }
          var con = 0

          var seriesS1 = [];
          var seriesS2 = [];
          var seriesS3 = [];
          var seriesS4 = [];
          var seriesS5 = [];

          for(s1 of arregloTempSem1){
            seriesS1.push([con, s1]);
            con+=1
          }
          con = 0
          for(s2 of arregloTempSem2){
            seriesS2.push([con, s2]);
            con+=1
          }
          con = 0
          for(s3 of arregloTempSem3){
            seriesS3.push([con, s3]);
            con+=1
          }
          con = 0
          for(s4 of arregloTempSem4){
            seriesS4.push([con, s4]);
            con+=1
          }
          con = 0
          for(s5 of arregloTempSem5){
            seriesS5.push([con, s5]);
            con+=1
          }

          chartLine.updateSeries( [{
            name: 'Temperatura Sem. 1',
            data: seriesS1
          }, {
            name: 'Temperatura Sem. 2',
            data: seriesS2
          }, {
            name: 'Temperatura Sem. 3',
            data: seriesS3
          }, {
            name: 'Temperatura Sem. 4',
            data: seriesS4
          }, {
            name: 'Temperatura Sem. 5',
            data: seriesS5
          }])

          chartColumn.updateSeries([{
            name: '',
            data:[tempSem1Data,tempSem2Data,tempSem3Data,tempSem4Data,tempSem5Data]
          }])
          

        }

      }

    }
  });  

  

}

window.setInterval(function () {

  iteration++;


  

  ajaxFUN()



}, 3000);


