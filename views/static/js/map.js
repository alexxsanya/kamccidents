function loadHeatMap(){
  /* Data points defined as an array of LatLng objects */
/* Data points defined as a mixture of WeightedLocation and LatLng objects */
  var heatMapData = [
    {location: new google.maps.LatLng(37.782, -122.447), weight: 0.5},
    new google.maps.LatLng(37.782, -122.445),
    {location: new google.maps.LatLng(37.782, -122.443), weight: 15},
    {location: new google.maps.LatLng(37.782, -122.441), weight: 3},
    {location: new google.maps.LatLng(37.782, -122.439), weight: 2},
    new google.maps.LatLng(37.782, -122.437),
    {location: new google.maps.LatLng(37.782, -122.435), weight: 0.5},
    {location: new google.maps.LatLng(37.785, -122.447), weight: 3},
    {location: new google.maps.LatLng(37.785, -122.445), weight: 7},
    new google.maps.LatLng(37.785, -122.443),
    {location: new google.maps.LatLng(37.785, -122.441), weight: 0.5},
    new google.maps.LatLng(37.785, -122.439),
    {location: new google.maps.LatLng(37.785, -122.437), weight: 2},
    {location: new google.maps.LatLng(37.785, -122.435), weight: 6}
  ];

  var sanFrancisco = new google.maps.LatLng(37.774546, -122.433523);

  map = new google.maps.Map(document.getElementById('mapCanvas'), {
    center: sanFrancisco,
    zoom: 15,
    mapTypeId: 'satellite'
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatMapData
  });

  heatmap.setMap(map);
}