(function($) {
	'use strict';

	/*------------------
		Preloder
	--------------------*/
	$(window).on('load', function() {
		$('#preloader').delay(550).fadeOut('slow');
		$('body').delay(550).css({
			'overflow': 'visible'
		});
	});


	/*------------------
		Navigation
	--------------------*/
	$('.menu-list').onePageNav();
	$('.nav-switch').on('click', function(event) {
		$('.mainmenu').toggleClass('active');
		$(this).toggleClass('active');
		event.preventDefault();
	});


	/*------------------
		PROGRESS BAR
	--------------------*/
	$('.progress-bar-style').each(function() {
		var progress = $(this).data("progress");
		var prog_width = progress + '%';
		if (progress <= 100) {
			$(this).append('<div class="bar-inner" style="width:' + prog_width + '"><span></span></div>');
		}
		else {
			$(this).append('<div class="bar-inner" style="width:100%"><span></span></div>');
		}
	});


	/*------------------
		ISOTOP JS
	--------------------*/
	$(window).on('load', function() {
		var grid_container = $('.portfolio_container'),
			grid_item = $('.grid-item');
		grid_container.imagesLoaded(function() {
			grid_container.isotope({
				itemSelector: '.grid-item',
				layoutMode: 'masonry'
			});
		});
		$('.portfolio-filter li').on('click', function(e) {
			$('.portfolio-filter li.active').removeClass('active');
			$(this).addClass('active');
			var selector = $(this).attr('data-filter');
			grid_container.isotope({
				filter: selector
			});
			return false;
			e.preventDefault();
		});
	});


	/*------------------
		MAGNIDIC POPUP
	--------------------*/
	$('.work-zoom').magnificPopup({
		type: 'inline',
		removalDelay: 400
	});


	/*------------------
		Review Carousel
	--------------------*/
	$('#testimonel-carousel').owlCarousel({
		dots: false,
		nav: true,
		loop: true,
		smartSpeed: 700,
		navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
		items: 1
	});


	/*------------------
		Contact Form
	--------------------*/
	$('#contact-form').on('submit', function() {
		var send_btn = $('#send-form'),
			form = $(this),
			formdata = $(this).serialize(),
			chack = $('#form-chack');
			send_btn.text('Wait...');

		function reset_form(){
		 	$("#name").val('');
			$("#email").val('');
			$("#massage").val('');
		}

		$.ajax({
			url:  $(form).attr('action'),
			type: 'POST',
			data: formdata,
			success : function(text){
				if (text == "success"){
					send_btn.addClass('done');
					send_btn.text('Success');
					setTimeout(function() {
						reset_form();
						send_btn.removeClass('done');
						send_btn.text('Massage');
					}, 2500);
				}
				else {
					reset_form();
					send_btn.addClass('error');
					send_btn.text('Error');
					setTimeout(function() {
						send_btn.removeClass('error');
						send_btn.text('Massage');
					}, 5000);
				}
			}
		});
		return false;
	});


	/*------------------
		WOW JS
	--------------------*/
	new WOW().init();


})(jQuery);