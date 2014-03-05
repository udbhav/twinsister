(function($) {
  $("body.home .feature .play").on("click", function(e) {
    e.preventDefault();

    $(this).toggleClass("playing");

    if ($(this).hasClass("playing")) {
      $(this).html("Pause");
    } else {
      $(this).html("Play");
    }

    $(".feature li").trigger("click");
  });

  $("body.home .feature .toggle-hide").on("click", function(e) {
    e.preventDefault();
    e.stopPropagation();
    $(".feature").addClass("minimal");
  });

  $("body.home").on("click", function(e) {
    $(".feature").removeClass("minimal");
  });
})(jQuery);
