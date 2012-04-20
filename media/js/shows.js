$(document).ready(function() {
    var latlng = new google.maps.LatLng(-34.397, 150.644);
    var myOptions = {
      zoom: 8,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("show_map"), myOptions);
    var bounds = new google.maps.LatLngBounds();
    var infowindow = new google.maps.InfoWindow({maxWidth: '400'});

    $(".content tr").each(function() {
        var latlng = $(this).attr("data-latlng").split(',');
        var position = new google.maps.LatLng(latlng[0], latlng[1]);
        
        bounds.extend(position);

        var marker = new google.maps.Marker({
            position: position, 
            map: map
        });  

        var info_content = $('<div class="info_content"></div>');
        info_content.html('<h3>' + $(this).find("td.date").html() + '</h3>' + $(this).find("td.title").html() + '<br/>' + $(this).find("td.venue").html() + '<br/>' + $(this).find("td.bands").html());
        marker.info_content = info_content[0];

        google.maps.event.addListener(marker, 'click', function() {
            infowindow.close()
            infowindow.setContent(marker.info_content);
            infowindow.open(map, marker);
        });

        map.fitBounds(bounds);
    });
});