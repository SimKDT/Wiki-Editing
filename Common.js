/* Any JavaScript here will be loaded for all users on every page load. */


/** 
 * Test if an element has a certain class 
 * 
 * Description: Uses regular expressions and caching for better performance.
 * Maintainers: [[User:Mike Dillon]], [[User:R. Koot]], [[User:SG]] 
 *   
var hasClass = ( function() {
	var reCache = {};
	return function( element, className ) {
		return ( reCache[className] ? reCache[className] : ( reCache[className] = new RegExp( "(?:\\s|^)" + className + "(?:\\s|$)" ) ) ).test( element.className );
	};
})();
** */

/**
 * Test if an element has a certain class
 * @deprecated:  Use $(element).hasClass() instead.
 */
mw.log.deprecate( window, 'hasClass', function ( element, className ) {
	return $( element ).hasClass( className );
}, 'Use jQuery.hasClass() instead' );

/* Template:Infobox/image */
window.addOnloadHook(function() {
  $('.infobox-image .infobox-gallery > *:first-child img').addClass('selected');
  $('.infobox-preview:first-child').show();
  $('.infobox-image .infobox-gallery > *').click(function() {
    var index = $(this).index();
    var previews = $(this).closest('.infobox-image').find('.infobox-preview');
    if (index < previews.length) {
      $(this).parent().find('img').removeClass('selected');
      $(this).find('img').addClass('selected');
      previews.hide();
      $(previews[index]).show();
    }
  });
});

/* Cycle through images with cycle-img */
$(function () {
    const visible = new Set();

    // Observe visible containers
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                visible.add(entry.target);
            } else {
                visible.delete(entry.target);
            }
        });
    }, {
        rootMargin: '200px 0px'
    });

    // Image cycling
    $('.cycle-img').each(function () {
        const images = $(this).children(
            'span[typeof="mw:File"], p:has(span[typeof="mw:File"])'
        );
        if (images.length < 2) return;
        this.cycleImages = images.toArray();
        this.cycleIndex = 0;
        this.cycleImages[0].classList.add('cycle-active');
        observer.observe(this);
    });

    // Cycle visible containers every 2 seconds
    setInterval(() => {
        visible.forEach(container => {
            const images = container.cycleImages;

            images[container.cycleIndex].classList.remove('cycle-active');
            container.cycleIndex = (container.cycleIndex + 1) % images.length;
            images[container.cycleIndex].classList.add('cycle-active');
        });
    }, 2000);
});

/* Template:Info (icon tooltip) */
window.addOnloadHook(function() {
    $(".tooltip-info-img").on("mouseover touchstart", function(e) {
        var tooltip = $(this).siblings('.tooltip-info-text');
        var windowWidth = $(window).width();

        if (windowWidth <= 600) {
            // Small screen
            var imageRect = $(this)[0].getBoundingClientRect();
            var tooltipHeight = tooltip.outerHeight();
            var tooltipWidth = tooltip.outerWidth();
            var tipY, tipX;

            if (imageRect.top > tooltipHeight + 10) {
                tipY = imageRect.top - tooltipHeight - 10;
            } else {
                tipY = imageRect.bottom + 10;
            }

            tooltip.css({
                top: tipY,
                left: tipX
            });
        } else {
            // Large screen
            var tooltip = $(this).siblings('.tooltip-info-text'); // Get tooltip element (tooltip-text)
            var tipX = $(this).outerWidth() + 5;             // 5px on the right of the tooltip
            var tipY = -40;                                  // 40px on the top of the tooltip
            tooltip.css({ top: tipY, left: tipX });          // Position tooltip

            // Get calculated tooltip coordinates and size
            var tooltip_rect = tooltip[0].getBoundingClientRect();
            // Corrections if out of window
            if ((tooltip_rect.x + tooltip_rect.width) > $(window).width()) { // Out on the right
                tipX = -tooltip_rect.width - 5; // Simulate a "right: tipX" position
            }
            if (tooltip_rect.y < 0) { // Out on the top
                tipY = tipY - tooltip_rect.y + 10; // Align on the top
            }

            // Apply corrected position
            tooltip.css({ top: tipY, left: tipX });
        }
    });
});
