//описываем свойства иконок для каждой группы маркеров
var myIcons = L.Icon.extend({
	options: {
		iconSize: [32, 37],
		iconAnchor: [20, 36],
		popupAnchor:  [-3, -30]
	}
});
var sanctuarysIcon = new myIcons({iconUrl: '/static/markers/fire.png'}),
	oldIcon = new myIcons({iconUrl: '/static/markers/ancienttempler.png'}),
	stonesIcon = new myIcons({iconUrl: '/static/markers/beautiful.png'}),
	etnoIcon = new myIcons({iconUrl: '/static/markers/crossingguard.png'}),
	springIcon = new myIcons({iconUrl: '/static/markers/diving.png'}),
	museumsIcon = new myIcons({iconUrl: '/static/markers/ancienttemple.png'}),
	treesIcon = new myIcons({iconUrl: '/static/markers/tree.png'}),
	attractionIcon = new myIcons({iconUrl: '/static/markers/attraction.png'});

//подключаем слои с маркерами
var sanctuarysLay = L.geoJson(sanctuarys, {
	pointToLayer: function (feature, latlng, name) {
		        return L.marker(latlng, {icon: sanctuarysIcon})
		}, onEachFeature: onEachFeature      
	});
var oldLay = L.geoJson(old, {
	pointToLayer: function (feature, latlng) {
		        return L.marker(latlng, {icon: oldIcon});
		}, onEachFeature: onEachFeature      
	});
var stonesLay = L.geoJson(stones, {
	pointToLayer: function (feature, latlng) {
		        return L.marker(latlng, {icon: stonesIcon});
		}, onEachFeature: onEachFeature      
	});
var springLay = L.geoJson(spring, {
	pointToLayer: function (feature, latlng) {
		        return L.marker(latlng, {icon: springIcon});
		}, onEachFeature: onEachFeature      
	});
var etnoLay = L.geoJson(etno, {
	pointToLayer: function (feature, latlng) {
		        return L.marker(latlng, {icon: etnoIcon});
		}, onEachFeature: onEachFeature      
	});
var museumsLay = L.geoJson(museums, {
	pointToLayer: function (feature, latlng) {
		        return L.marker(latlng, {icon: museumsIcon});
		}, onEachFeature: onEachFeature      
	});
var treesLay = L.geoJson(trees, {
	pointToLayer: function (feature, latlng) {
		        return L.marker(latlng, {icon: treesIcon});
		}, onEachFeature: onEachFeature      
	});
var attractionLay = L.geoJson(attraction, {
	pointToLayer: function (feature, latlng) {
		        return L.marker(latlng, {icon: attractionIcon});
		}, onEachFeature: onEachFeature      
	});

//подключаем базовые слои	
var humanitarian = L.tileLayer('http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'});
var esriSat = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.jpg', {
	attribution: '&copy; <a href="https://www.esri.com/about-esri/">Esri</a>'});
var openTopo = L.tileLayer('http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="https://opentopomap.org/about">OpenTopoMap</a>'});
var map1eu = L.tileLayer('http://beta.map1.eu/tiles/{z}/{x}/{y}.jpg', {
	attribution: '&copy; <a href="http://beta.map1.eu/">Map of Europe</a>'});
		
//отображаем карту, устанавливаем дефолтные параметры	
var map = new L.map('map', {
  center: [49.002390, 30.658259], 
  zoom: 7,
  layers: humanitarian,
  maxBounds: ([[52.389588, 17.0], [44.254408, 40.258236]]),
  fullscreenControl: true, //подключаем кнопку Full screen
  fullscreenControlOptions: {
  position: 'topleft'
  }
}); 
		
var hash = new L.Hash(map); //подключили отображение координат в строке адреса
L.control.defaultExtent().addTo(map); //подключили кнопку "Домой""

//пробуем кластеризовать
var mcgLayerSupportGroup = L.markerClusterGroup.layerSupport();
var markersCluster = L.layerGroup();
markersCluster.addLayer(sanctuarysLay);
markersCluster.addLayer(oldLay);
markersCluster.addLayer(stonesLay);
markersCluster.addLayer(springLay);
markersCluster.addLayer(etnoLay);
markersCluster.addLayer(museumsLay);
markersCluster.addLayer(treesLay);
markersCluster.addLayer(attractionLay);
//map.addLayer(markersCluster);
 
//включаем переключатель слоёв
mcgLayerSupportGroup.addTo(map);
mcgLayerSupportGroup.checkIn(markersCluster);
markersCluster.addTo(map);
L.control.layers({
	'Humanitarian':humanitarian, 'Супутник':esriSat, 'Map1.eu':map1eu, 'OpenTopoMap':openTopo
	}, 
	{
	'Капища і храми':sanctuarysLay, 'Старовинні святилища':oldLay, 'Гори, камені, печери':stonesLay, 'Джерела':springLay, 'Етнозаходи':etnoLay, 'Музеї':museumsLay, 'Дерева':treesLay, 'Атракції':attractionLay
	}).addTo(map);

//настраиваем поиск по маркерам
L.control.search({
		layer: markersCluster,
		initial: false,
		propertyName:'name'
	}).addTo(map);

//тушим некоторые слои с маркерами
museumsLay.remove();
etnoLay.remove();
treesLay.remove();
attractionLay.remove();

var sidebar = L.control.sidebar('sidebar', {
            closeButton: true,
            position: 'left',
			autoPan: true
        });
        map.addControl(sidebar);

//обработчик события - нажатие на маркер, показывает pop-up
function onEachFeature(feature, layer) {
	layer.on({
		mouseover:layer.bindTooltip(feature.properties.name),
		click:function sideDescription(){
			sidebar.show();
			sidebar.setContent(feature.properties.description);
		}
	})
	
/*	if (feature.properties && feature.properties.description) {
		layer.bindPopup(feature.properties.description, {maxWidth:500});
		layer.bindTooltip(feature.properties.name);
	}*/
};

//кнопка добавления маркера
L.easyButton('fa-map-marker', function(){
    sidebar.show();
    document.getElementById('form-elements').style.display = "block";
    document.getElementById('thankyou_message').style.display = "none";
	document.getElementById('name').value = null;
	document.getElementById('message').value = null;
	var noteMarker = L.marker(map.getCenter(), {
		draggable: true,
		autoPan: true
		}).addTo(map);
	var markerLatLng = noteMarker.getLatLng();
	document.getElementById('longitude').value = markerLatLng.lng;
	document.getElementById('latitude').value = markerLatLng.lat;
	document.getElementById('zoom').value = map.getZoom();
	noteMarker.on('dragend', function(){
			var markerLatLng = this.getLatLng();
			document.getElementById('longitude').value = markerLatLng.lng;
			document.getElementById('latitude').value = markerLatLng.lat;
			document.getElementById('zoom').value = map.getZoom()
	});
	map.on('click', function(ev){
	var markerLatLng = ev.latlng;
	document.getElementById('longitude').value = markerLatLng.lng;
	document.getElementById('latitude').value = markerLatLng.lat;
	document.getElementById('zoom').value = map.getZoom();	
	noteMarker.setLatLng(markerLatLng)	;
	});
	sidebar.on('hidden', function(){
	noteMarker.remove();
	});
},
'Додати нотатку').addTo(map);


