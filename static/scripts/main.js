let map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 39.6, lng: -8.093},
        zoom: 7
    });
    $.getJSON("data.json", function(json) {
        json['stations'].forEach(function(element) {
            let marker = new google.maps.Marker({
                position: {
                    lat: element['location'][0],
                    lng: element['location'][1]
                },
                map : map,
            });
            marker.addListener('click', function(){
                if (map.getZoom() < 11) {
                    map.setZoom(11);
                }
                map.panTo(marker.getPosition());
                fillInfo(element)
            });
        });
    });
};


function fillInfo(station) {
    document.getElementById('name').innerHTML =  '<a href="'+ station.url +'" target="_blank">' + station.name + '<i class="fas fa-external-link-alt"></i></a>';

    document.getElementById('basic-info').innerHTML = '<li><strong>Morada: </strong>' + station.address + '</li>';
    document.getElementById('basic-info').innerHTML += '<li><strong>Coordenadas: </strong>' + station.location[0] + ' | ' + station.location[1] + '</li>';
    if(station.cp_services != null){
        cp_services = station.cp_services.toString().replace(/,/g, ' | ');
        document.getElementById('basic-info').innerHTML += '<li><strong>Serviços CP: </strong>' + cp_services + '</li>';
    }
    if(station.lines != null) {
        lines = station.lines.toString().replace(/,/g, ' | ');
        document.getElementById('basic-info').innerHTML += '<li><strong>Linhas: </strong>' + lines + '</li>';
    }

    services = ['cp_services', 'access_connections', 'facilities', 'complementary_services'];

    if(station.services != null) {
        document.getElementById('accordion').hidden = false;
        index = 0;
        services.forEach(function(service) {
            if(station.services.hasOwnProperty(service)){
                if(index == 0) {
                    document.getElementById(service).querySelector('div button').classList.remove('collapsed');
                    document.getElementById(service).querySelector('div .collapse').classList.add('show');
                    index++;
                }
                else{
                    document.getElementById(service).childNodes[3].classList.remove('show');
                    document.getElementById(service).childNodes[1].querySelector('button').classList.add('collapsed');
                }
                document.getElementById(service).querySelector('ul').innerHTML = '';
                station.services[service].forEach(function(element){
                    document.getElementById(service).querySelector('ul').innerHTML += '<li class="list-group-item">' + element + '</li>';
                });
                document.getElementById(service).hidden = false;
            }
            else {
                document.getElementById(service).hidden = true;
            }
        });
    }
    else {
        document.getElementById('accordion').hidden = true;
    }
    document.getElementById('station-container').hidden = false;
}

$('#station-container .close').click(function (){
    document.getElementById('station-container').hidden = true;
});
