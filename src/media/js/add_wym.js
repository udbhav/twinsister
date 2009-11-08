$(document).ready(function() {
    $("textarea").wymeditor({
        stylesheet: '/media/css/wymeditor.css',
        updateSelector: "input:submit",
        updateEvent:    "click",
    });
});