$(window).load(function(){
    // Isotope
    $(function(){
        var $container = $('.gallery_image_container');

        $container.isotope({
            itemSelector: '.gallery_image_item',
            layoutMode: 'cellsByRow',
            cellsByRow: {
                columnWidth: 360,
                rowHeight: 360
            }
        });
    });
});

$(document).ready(function() {
    $('.gallery_image_item').click(function() {
        $(this).toggleClass('selected');
        var thumb = $(this).find('.gallery_thumbnail')
        thumb.hide();
        thumb.fadeIn(800);
    });
});
