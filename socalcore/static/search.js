function search() {	var cat = $('#search').val();    var loc = $('#boroughs option:selected').val().split(',');    latitude = loc[0];    longitude = loc[1];	jQuery.get('/search/' + cat + "/" + longitude + "," + latitude, showResults);}function showResults(data) {	$('#results').html();	$('#map').gmap3(        {action: 'clear'}    )	$('#results').html(data);}