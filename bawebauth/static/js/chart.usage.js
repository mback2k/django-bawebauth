$(document).ready(function() {
  if (typeof charts == 'undefined') return;
  $.each(charts || {}, function(key, value) {
    $.getJSON(value, function(json) {
      var chart = new google.visualization.AnnotatedTimeLine(document.getElementById(key));
      var data = new google.visualization.DataTable();
      var data_latest = new Date(0);
      var data_previous = null;

      data.addColumn('datetime', 'Date');
      data.addColumn('number', 'Send');
      data.addColumn('number', 'Received');

      $.each(json, function(key, value) {
        var data_crdate = new Date(); data_crdate.setISO8601(value.fields.crdate.replace(/ /, 'T'));
        if (data_crdate > data_latest) data_latest = new Date(data_crdate.getTime());
        if (data_previous != null && ((data_crdate - data_previous) > (1000 * 60 * 10))) {
          var data_fix1 = new Date(data_previous.getTime());
          var data_fix2 = new Date(data_crdate.getTime());
          data_fix1.setMinutes(data_previous.getMinutes()+5);
          data_fix2.setMinutes(data_crdate.getMinutes()-5);
          data.addRows([[data_fix1, 0, 0]]);
          data.addRows([[data_fix2, 0, 0]]);
        }
        data_previous = new Date(data_crdate.getTime());
        data.addRows([[data_crdate, value.fields.send, value.fields.received]]);
      });

      var date_start = new Date(data_latest.getTime());
      var date_end = new Date(data_latest.getTime());

      date_start.setDate(date_end.getDate()-1);

      chart.draw(data, {
        'allowRedraw': true,
        'scaleType': 'maximized',
        'zoomStartTime': date_start,
        'zoomEndTime': date_end,
      });
    });
  });
});