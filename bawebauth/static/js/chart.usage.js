$(document).ready(function() {
  $('.highchart').each(function(index, chart) {
    chart = $(chart);

    $.getJSON(chart.attr('href'), function(json) {
      chart.animate({'width': '100%', 'height': '280px'}).css('opacity', 0).progressbar({value: 0});

      var options = {
        chart: {
          renderTo: chart.attr('id'),
          zoomType: 'x',
          type: 'areaspline'
        },
        title: {
          text: 'Traffic Usage'
        },
        xAxis: {
          text: 'Usage in Bytes',
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

      var queue = $({});
      var previous = null;

      $.each(json, function(index, point) {
        queue.queue('stack', function() {
          var crdate = new Date().setISO8601(point.fields.crdate).getTime();
          if (previous != null && ((crdate - previous) > 600000)) {
            var fix1 = [previous - 1000, null];
            var fix2 = [previous + 1000, null];

            options.series[0].data.push(fix1);
            options.series[0].data.push(fix2);
            options.series[1].data.push(fix1);
            options.series[1].data.push(fix2);
          }
          previous = crdate;

          options.series[0].data.push([crdate, point.fields.send]);
          options.series[1].data.push([crdate, point.fields.received]);

          var progress = index / json.length;
          chart.css('opacity', progress).progressbar({value: progress*100});

          setTimeout(function() {
            queue.dequeue('stack');
          }, 1);
        });
      });

      queue.queue('stack', function() {
        chart.data('highchart', new Highcharts.Chart(options)).css('opacity', 1);
      });

      queue.dequeue('stack');
    });
  });
});