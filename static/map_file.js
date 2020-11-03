osm=new ol.layer.Tile({
    title: 'OpenStreetMap',
    type: 'base',
    visible: false,
    source: new ol.source.OSM()
})

streets=new ol.layer.Tile({
title:"Streets",
type:'base',
visible:false,
source: new ol.source.XYZ({
    url: 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZGV2MjAwMCIsImEiOiJja2Nwczk5cjUweHp4MnFzNnc0cXpuc3Y2In0.3lT6qtv5vpyMG4HMhk-FPg'
    })
})


sat= new ol.layer.Tile({
title:"Satellite",
type:'base',
// visible:false,
source: new ol.source.XYZ({
    url: 'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZGV2MjAwMCIsImEiOiJja2Nwczk5cjUweHp4MnFzNnc0cXpuc3Y2In0.3lT6qtv5vpyMG4HMhk-FPg'
    })
})

var base_lyr=new ol.layer.Group({
    title: 'Base maps',
    layers: [osm,streets,sat ]
})

var map = new ol.Map({
    // controls: ol.control.defaults().extend([mousePositionControl]),
    target: 'map',
    layers: [base_lyr],
    view: new ol.View({
        center: [8757325.249121, 1958618.264098],
        zoom: 5,
    })
});



