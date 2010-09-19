$(document).ready(function() {
    // Track Song plays on Google Analytics
    $(".playlist a").click(function() {
        _gaq.push(['_trackEvent', 'Songs', 'Play', $(this).html()]);
    });

    // Track Release downloads on Google Analytics
    $(".download_links a").click(function() {
        var label = $(this).attr("title") + ' ' + $(this).html();
        _gaq.push(['_trackEvent', 'Releases', 'Download', label]);
    });
});