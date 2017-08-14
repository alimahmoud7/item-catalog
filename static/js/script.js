// To make active class work
$('.field-list').on('click', 'li', function() {
    $('.field-list li.active').removeClass('active');
    $(this).addClass('active');
});
