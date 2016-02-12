jQuery(function($) {'use strict';

	//Responsive Nav
	$('li.dropdown').find('.fa-angle-down').each(function(){
		$(this).on('click', function(){
			if( $(window).width() < 768 ) {
				$(this).parent().next().slideToggle();
			}
			return false;
		});
	});

	//Fit Vids
	if( $('#video-container').length ) {
		$("#video-container").fitVids();
	}

	$(function() {
		var pgurl = window.location.href.substr(window.location.href.lastIndexOf("/")+1);
		
		$("#header ul li").each(function(){
	     	if($('a', this).attr("href") == pgurl || $('a', this).attr("href") == ''){
	     		$(this).addClass("active");
		    }
		})
	});

	
    $(document).ready(function() {
        function isScrolledTo(elem) {
            var docViewTop = $(window).scrollTop(); //num of pixels hidden above current screen
            var docViewBottom = docViewTop + $(window).height();
 
            var elemTop = $(elem).offset().top; //num of pixels above the elem
            var elemBottom = elemTop + $(elem).height();
 
            return ((elemTop <= docViewTop));
        }
 
        var catcher = $('#catcher');
        var sticky = $('#sticky');
        sticky.css('position','fixed');
        sticky.css('position','absolute'); //quick fix

        $(window).scroll(function() {
        	if ($('#sticky'))
        	{
	            if(isScrolledTo(sticky)) {
	                sticky.css('position','fixed');
	                sticky.css('top','0px');
	            }
	            var stopHeight = catcher.offset().top + catcher.height();
	            if ( stopHeight > sticky.offset().top) {
	                sticky.css('position','absolute');
	                sticky.css('top',stopHeight);
	            }
	        }
        });
    });

	//Initiat WOW JS
	new WOW().init();

	// portfolio filter
	$(window).load(function(){

		$('.main-slider').addClass('animate-in');
		$('.preloader').remove();
		//End Preloader

		if( $('.masonery_area').length ) {
			$('.masonery_area').masonry();//Masonry
		}

		var $portfolio_selectors = $('.portfolio-filter >li>a');

		if($portfolio_selectors.length) {

			var $portfolio = $('.portfolio-items');
			$portfolio.isotope({
				itemSelector : '.portfolio-item',
				layoutMode : 'fitRows'
			});

			$portfolio_selectors.on('click', function(){
				$portfolio_selectors.removeClass('active');
				$(this).addClass('active');
				var selector = $(this).attr('data-filter');
				$portfolio.isotope({ filter: selector });
				return false;
			});
		}

	});


	$('.timer').each(count);
	function count(options) {
		var $this = $(this);
		options = $.extend({}, options || {}, $this.data('countToOptions') || {});
		$this.countTo(options);
	}

	// Search
	$('.fa-search').on('click', function() {
		$('.field-toggle').fadeToggle(200);
	});

	// Contact form
	var form = $('#main-contact-form');
	form.submit(function(event){
		//event.preventDefault();
		var form_status = $('<div class="form_status"></div>');
		$.ajax({
			url: $(this).attr('action'),
			beforeSend: function(){
				form.prepend( form_status.html('<p><i class="fa fa-spinner fa-spin"></i> Email is sending...</p>').fadeIn() );
			}
		}).done(function(data){
			form_status.html('<p class="text-success">Message sent. Thank you.</p>').delay(3000).fadeOut();
		});
	});

	// Progress Bar
	$.each($('div.progress-bar'),function(){
		$(this).css('width', $(this).attr('data-transition')+'%');
	});
	var map;
	if( $('#gmap').length ) {
	    map = new GMaps({
	        el: '#gmap',
	        lat: 33.645371,
		    lng: -117.844726
	    });
	    map.addMarker({
            lat: 33.645371,
            lng: -117.844726,
            title: 'Parker Lab UCI'
        });
	}

});