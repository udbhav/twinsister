$(document).ready(function() {
    $(".pagination").hide();
    $.autopager({
        link: '.next_page',
        content: '#autopager_content'
    });
});