$(document).ready(function() {
    // Track Song plays on Google Analytics
    $(".playlist a").click(function() {
        _gaq.push(['_trackEvent', 'Songs', 'Play', $(this).html()]);
        console.log('test');
    });

    // Track Release downloads on Google Analytics
    $(".download_links a").click(function() {
        var label = $(this).attr("title") + ' ' + $(this).html();
        _gaq.push(['_trackEvent', 'Releases', 'Download', label]);
    });

    // Track Release purchases on Google Analytics
    $(".buy_links a").click(function() {
        var label = $(this).attr("title") + ' ' + $(this).html();
        _gaq.push(['_trackEvent', 'Releases', 'Buy', label]);
    });

});