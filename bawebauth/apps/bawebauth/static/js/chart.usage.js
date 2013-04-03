$(document).ready(function() {
  $('.chart.usage').each(function(index, chart) {
    chart = $(chart);

    $.getJSON(chart.find('a').attr('href'), function(json) {
      chart.css('width', '100%').css('height', '400px').css('opacity', 0).progressbar({value: 0});

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
          min: 0,
          title: {
            text: 'Usage in Bytes'
          }
        },
        rangeSelector: {
          buttons: [{
            type: 'day',
            count: 3,
            text: '3d'
          }, {
            type: 'week',
            count: 1,
            text: '1w'
          }, {
            type: 'month',
            count: 1,
            text: '1m'
          }, {
            type: 'month',
            count: 6,
            text: '6m'
          }, {
            type: 'year',
            count: 1,
            text: '1y'
          }, {
            type: 'all',
            text: 'All'
          }],
          selected: 1
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
        series: [{
            name: 'Send',
            data: [],
            fillColor: {
              stops: [
                [0, '#4572A7'],
                [1, 'rgba(0,0,0,0)']
              ]
            }
          }, {
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
            var fixes = [
              [previous - 300000, null],
              [previous + 300000, null]
            ];
            $.each(fixes, function(index, fix) {
              options.series[0].data.push(fix);
              options.series[1].data.push(fix);
            });
          }
          previous = crdate;

          options.series[0].data.push([crdate, point.fields.send]);
          options.series[1].data.push([crdate, point.fields.received]);

          var progress = index / json.length;
          chart.css('opacity', progress).progressbar({value: progress*100});

          window.setZeroTimeout(function() {
            queue.dequeue('stack');
          });
        });
      });

      queue.queue('stack', function() {
        chart.data('highchart', new Highcharts.StockChart(options)).css('opacity', 1);
      });

      queue.dequeue('stack');
    });
  });
});