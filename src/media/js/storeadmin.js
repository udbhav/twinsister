$(document).ready(function() {
    $(".ship_order").click(function(e) {
        e.preventDefault();
        var link = this;
        $.post("/store/admin/ship-order/", {pk: $(this).attr('data-order-id')}, function(data) {
            $(link).parents("tr").fadeOut();
        });
    })
});