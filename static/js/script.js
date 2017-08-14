// To make active class work
$(document).ready(function(){
  $(".field-list li").each(function(){
    var href = $(this).find('a').attr('href');
    if (href === window.location.pathname) {
      $(this).addClass('active');
    }
  });
});
