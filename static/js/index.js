$(document).ready(function() {

	var curves = [ {
		color : "green",
		data : [],
		bars : {
			show : true,
			fill : 1
		},
		points : {
			show : true
		},
		xaxis : {
			show : true
		},
		label : "Positive emotion signal"
	}, {
		color : "red",
		data : [],
		bars : {
			show : true,
			fill : 1
		},
		points : {
			show : true
		},
		label : "Negative emotion signal"
	}, {
		color : "grey",
		data : [],
		lines : {
			show : true,
		},
		label : "Average impact (average pos+neg)"
	}, {
		color : "blue",
		data : [],
		lines : {
			show : true,
		},
		label : "Average opinion (average pos-neg)"
	} ];
	var plot = $.plot($("#chart"), curves);

	var last_timestamp = null;

	var get_latest = function() {

		$.getJSON("/api/latest", function(pairs) {

			if (last_timestamp == null || pairs[0][2] > last_timestamp) {
				last_timestamp = pairs[0][2];
				var message = jQuery('<div/>', {
					'class': 'alert',
					'html': 'New twit received!'
				}).appendTo('#messages');
				message.fadeIn(500).delay(2000).fadeOut(500, function() {
					$(this).remove();
				});
			}

			curves[0].data = [];
			curves[1].data = [];
			curves[2].data = [];
			curves[3].data = [];

			var pos_data = curves[0].data;
			var neg_data = curves[1].data;
			var avg_data = curves[2].data;
			var int_data = curves[3].data;

			var avg = 0;
			var int = 0;
			pairs = pairs.reverse();

			jQuery.each(pairs.slice(0, pairs.length), function(index, pair) {
				var pos = pair[0];
				var neg = pair[1];
				var timestamp = pair[2];
				var datum1 = [ timestamp, pos ];
				var datum2 = [ timestamp, -neg ];

				avg = (avg * index + (pos + neg)) / (index + 1);
				var datum3 = [ timestamp, avg ];

				int += pos - neg;
				var datum4 = [ timestamp, int / (index + 1) ]

				pos_data.push(datum1);
				neg_data.push(datum2);
				avg_data.push(datum3);
				int_data.push(datum4);

			});
			plot.setData(curves);
			plot.setupGrid();
			plot.draw();

			setTimeout(get_latest, 2500);

		});
	}
	get_latest();

});