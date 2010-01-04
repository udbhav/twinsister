$(document).ready(function() {
    $("body").mousemove(function() {
        if ($(".release_info").css("opacity") == 0) {
            $(".release_info, h3, #more_link").animate({"opacity": "100"}, 7000);
        }
    });
});