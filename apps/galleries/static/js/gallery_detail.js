// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );



});

$(function(){
    var $container = $('.gallery_image_container');

    $container.isotope({
        itemSelector: '.gallery_image_item',
        layoutMode : 'masonry',
        masonry: {
            columnWidth: 320
          }
    });
});