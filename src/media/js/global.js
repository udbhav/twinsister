$(document).ready(function() {
    $(".pagination").hide();
    $.autopager({
        link: '.next_page',
        content: '#autopager_content'
    });

    // Track Song plays on Google Analytics
    $(".tracklist a").click(function() {
        _trackEvent("Songs", "Play", $(this).html());
    });

    // Track Release downloads on Google Analytics
    $(".download_links a").click(function() {
        var label = $(this).attr("title") + ' ' + $(this).html();
        _trackEvent("Releases", "Download", label);
});