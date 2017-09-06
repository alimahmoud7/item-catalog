// To make active class work
$(function () {
    $('.field-list li').each(function () {
        $(this).removeClass('active');
        var href = $(this).find('a').attr('href');
        if (href === window.location.pathname) {
            $(this).addClass('active');
        }
        else if (window.location.pathname === '/') {
			$('#all-fields').addClass('active');
		}
    });
});
