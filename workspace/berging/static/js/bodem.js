var BODEM = {
var geojson;
var map;
var info = L.control();

function fitAddress(map, address) {
	var geocoder = new google.maps.Geocoder();
	if (geocoder) {
	   geocoder.geocode({ 'address': address }, function (results, status) {
	     if (status == google.maps.GeocoderStatus.OK) {
	         var b = results[0].geometry.viewport;
	         var ne = b.getNorthEast();
	         var sw = b.getSouthWest();
	         map.fitBounds([[sw.lat(), sw.lng()],
	                        [ne.lat(), ne.lng()]]);	     
	     }
	   });
	}
}

function getColor(d) {
	//var colors = [0,'pink','yellow', 'green', 'green', 'green', 'blue', 'red'];
	var colors = [0,'#FF3399','#FFFF66', '#99FF66', '#009900', '#339966', '#006666', '#CC0000'];
	var i = Number(d);
	if (i >= 1 && i <= 7)
		return colors[d];
	return 'white';
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.GRONDSOORT),
         weight: 1,
         opacity: 1,
         color: 'None',
        fillOpacity: 0.4
    };
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 1,
        color: 'white',
        dashArray: '',
        fillOpacity: 0.8
    });

    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

function initialize() {
	map = new L.Map('map');
	fitAddress(map,'Noord-Holland');
	var osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
	var ggl = new L.Google();
	var ggl1 = new L.Google('ROADMAP');
	var ggl2 = new L.Google('TERRAIN');
	grondsoort = {{grondsoort|safe}};
	geojson = new L.geoJson(grondsoort, {
        style: style,
        onEachFeature: onEachFeature
    });
	var baseMaps = {'Open Streetmap':osm, 'Google':ggl1, 'Satelliet': ggl, 'Terrein':ggl2};
	var overlayMaps = {'Grondsoort': geojson };
	L.control.layers(baseMaps, overlayMaps).addTo(map);	
	map.addLayer(osm);
	map.addLayer(geojson);

	info.onAdd = function (map) {
	    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
	    this.update();
	    return this._div;
	};
	info.update = function (props) {
		if (props) {
	    	this._div.innerHTML = '<h4>Grondsoort: ' +  props.NAAM + '</h4>';
			this._div.style.display='block';
		}
		else
			this._div.style.display='none';
	};

	info.addTo(map);
}
};
