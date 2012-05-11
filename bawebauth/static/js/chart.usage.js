$(document).ready(function() {
  $('.highchart').each(function(index, chart) {
    $.getJSON($(chart).attr('href'), function(json) {
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
          maxZoom: 300000,
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

      var data_latest = new Date(0);
      var data_previous = null;

      $.each(json, function(key, value) {
        var data_crdate = new Date(); data_crdate.setISO8601(value.fields.crdate.replace(/ /, 'T'));
        if (data_crdate > data_latest) data_latest = new Date(data_crdate.getTime());
        if (data_previous != null && ((data_crdate - data_previous) > (1000 * 60 * 10))) {
          var data_fix1 = new Date(data_previous.getTime());
          var data_fix2 = new Date(data_crdate.getTime());
          data_fix1.setMinutes(data_previous.getMinutes()+5);
          data_fix2.setMinutes(data_crdate.getMinutes()-5);

          options.series[0].data.push([data_fix1.getTime(), 0]);
          options.series[1].data.push([data_fix1.getTime(), 0]);
          options.series[0].data.push([data_fix2.getTime(), 0]);
          options.series[1].data.push([data_fix2.getTime(), 0]);
        }
        data_previous = new Date(data_crdate.getTime());

        options.series[0].data.push([data_crdate.getTime(), value.fields.send]);
        options.series[1].data.push([data_crdate.getTime(), value.fields.received]);
      });

      var date_start = new Date(data_latest.getTime());
      var date_end = new Date(data_latest.getTime());

      date_start.setDate(date_end.getDate()-1);

      new Highcharts.Chart(options);
    });
  });
});