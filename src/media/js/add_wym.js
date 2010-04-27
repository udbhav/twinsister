$(document).ready(function() {
    $("textarea").wymeditor({
        stylesheet: '/media/css/wymeditor.css',
        updateSelector: "input:submit",
        updateEvent:    "click",
        postInit: function(wym) {
            var textarea = $(wym._element);
            if (textarea.attr("id") == "id_intro") {
                var parent = textarea.closest("div");
                var wym_box = parent.find(".wym_box");
                wym_box.hide();
                var a = $(document.createElement('a')).attr("href", "#").html("Show/Hide").bind("click", function() {
                    wym_box.toggle();
                    return false;
                });
                parent.find("label").after(a);
            }
        }
    });
});