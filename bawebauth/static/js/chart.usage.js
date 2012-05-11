$(document).ready(function() {
  $('.highchart').each(function(index, chart) {
    $(chart).progressbar({
      value: 5
    });
    $.getJSON($(chart).attr('href'), function(json) {
      $(chart).progressbar({value: 10});

      var options = {
        chart: {
          renderTo: $(chart).attr('id'),
          zoomType: 'x',
          type: 'areaspline'
        },
        title: {
          text: 'Traffic Usage'
        },
        xAxis: {
          type: 'datetime',
          maxZoom: 30000,
          dateTimeLabelFormats: { // don't display the dummy year
            second: '%H:%M:%S',
            minute: '%H:%M',
            hour: '%H:%M',
            day: '%e. %b',
            week: '%e. %b',
            month: '%b \'%y',
            year: '%Y'
          }
        },
        yAxis: {
          min: 0
        },
        plotOptions: {
          areaspline: {
            fillOpacity: 0.5,
            fillColor: {
              linearGradient: [0, 0, 0, 300],
            },
            lineWidth: 1,
            marker: {
              enabled: false,
              states: {
                hover: {
                  enabled: true,
                  radius: 3
                }
              }
            },
            shadow: false,
            states: {
              hover: {
                lineWidth: 1
              }
            }
          }
        },
        series: [
          {
            name: 'Send',
            data: [],
            fillColor: {
              stops: [
                [0, '#4572A7'],
                [1, 'rgba(0,0,0,0)']
              ]
            }
          },
          {
            name: 'Received',
            data: [],
            fillColor: {
              stops: [
                [0, '#A74472'],
                [1, 'rgba(0,0,0,0)']
              ]
            }
          }
        ]
      };

      var data_previous = null;

      $.each(json, function(key, value) {
        var data_crdate = new Date(); data_crdate.setISO8601(value.fields.crdate);
        if (data_previous != null && ((data_crdate.getTime() - data_previous.getTime()) > 600000)) {
          options.series[0].data.push([data_previous.getTime()-1000, null]);
          options.series[0].data.push([data_previous.getTime()+1000, null]);
          options.series[1].data.push([data_previous.getTime()-1000, null]);
          options.series[1].data.push([data_previous.getTime()+1000, null]);
        }
        data_previous = new Date(data_crdate.getTime());

        options.series[0].data.push([data_crdate.getTime(), value.fields.send]);
        options.series[1].data.push([data_crdate.getTime(), value.fields.received]);

        console.log(((key/json.length)*80)+10);
        $(chart).progressbar({value: ((key/json.length)*80)+10});
      });

      $(chart).progressbar({value: 90});
      $(chart).data('highchart', new Highcharts.Chart(options));
    });
  });
});