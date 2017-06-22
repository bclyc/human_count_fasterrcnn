$( document ).ready( function(){
	$('.slides ul').jcarousel({
		scroll: 1,
		wrap: 'both',
		initCallback: _init_carousel,
		buttonNextHTML: null,
		buttonPrevHTML: null
	});
});

function _init_carousel(carousel) {
	$('.slider-nav .next').bind('click', function() {
		carousel.next();
		return false;
	});
	
	$('.slider-nav .prev').bind('click', function() {
		carousel.prev();
		return false;
	});
};