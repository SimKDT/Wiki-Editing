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



/* ============================================================
   ZedScripts syntax highlighting

   Usage: 
   <syntaxhighlight lang="text" class="zedscripts">
   item ID {
     param1 = value1,
   }
   </syntaxhighlight>

   Original implementation:
   https://github.com/PZ-Wiki-Modding/ZedScripts-LSP/blob/main/src%2FZedScripts%2Fstructure%2Fpygments_lexer.py
   ============================================================ */

(function () {
    /** Token creation */
    function addToken(parent, className, text) {
        if (!text) {
            return;
        }

        const span = document.createElement('span');

        if (className) {
            span.className = className;
        }

        span.textContent = text;
        parent.appendChild(span);
    }

    /** ZedScripts lexer */
    function highlightZedScripts(source) {
        const output = document.createDocumentFragment();
        let pos = 0;

        const attribute =
            /(\S+[\S/ ]*?)(\s*)(=)(\s*)/y;

        const declaration =
            /^(\s*)(\w+)(\s+)(|[\w !*.:/]+?)(\s*)({)(\s*)$/;

        const declarationWithoutBrace =
            /^(\s*)(\w+)(\s+)(|[\w !*.:/]+?)(\s*)$/;

        while (pos < source.length) {

            const rest = source.slice(pos);

            // Multiline comments
            if (source.startsWith('/*', pos)) {
                let end = source.indexOf('*/', pos + 2);

                end = end === -1
                    ? source.length
                    : end + 2;

                addToken(
                    output,
                    'cm',
                    source.slice(pos, end)
                );

                pos = end;
                continue;
            }

            // Declaration lines
            if (pos === 0 || source[pos - 1] === '\n') {
                let end = source.indexOf('\n', pos);

                if (end === -1) {
                    end = source.length;
                }

                const line = source.slice(pos, end);

                let match = line.match(declaration);

                // Also support opening braces on the next line
                if (!match && end < source.length) {
                    const nextEnd = source.indexOf('\n', end + 1);

                    const nextLine = source.slice(
                        end + 1,
                        nextEnd === -1
                            ? source.length
                            : nextEnd
                    );

                    if (/^[ \t]*\{[ \t]*$/.test(nextLine)) {
                        match = line.match(declarationWithoutBrace);
                    }
                }

                if (match) {
                    addToken(output, 'w', match[1]);
                    addToken(output, 'kd', match[2]);
                    addToken(output, 'w', match[3]);
                    addToken(output, 'nc', match[4]);
                    addToken(output, 'w', match[5]);

                    // Opening brace on the same line
                    if (match[6] !== undefined) {
                        addToken(output, 'o', match[6]);
                        addToken(output, 'w', match[7]);
                    }

                    pos = end;
                    continue;
                }
            }

            // Operators
            if (/[,;:|!={}\[\]]/.test(source[pos])) {
                addToken(output, 'o', source[pos]);
                pos++;
                continue;
            }

            // Attribute assignments
            attribute.lastIndex = pos;

            const attr = attribute.exec(source);

            if (attr) {
                addToken(output, 'na', attr[1]);
                addToken(output, 'w', attr[2]);
                addToken(output, 'o', attr[3]);
                addToken(output, 'w', attr[4]);

                pos = attribute.lastIndex;
                continue;
            }

            // Floating-point numbers
            let match = rest.match(/^-?\d+\.\d+/);

            if (
                match &&
                (pos === 0 || !/\w/.test(source[pos - 1]))
            ) {
                addToken(output, 'mf', match[0]);
                pos += match[0].length;
                continue;
            }

            // Integers
            match = rest.match(/^-?\d+/);

            if (
                match &&
                (pos === 0 || !/\w/.test(source[pos - 1]))
            ) {
                addToken(output, 'mi', match[0]);
                pos += match[0].length;
                continue;
            }

            // Dotted identifiers
            match = rest.match(/^\w+\.\w+/);

            if (match) {
                addToken(output, 's2', match[0]);
                pos += match[0].length;
                continue;
            }

            // Whitespace (excluding newlines)
            match = rest.match(/^[^\S\n]+/);

            if (match) {
                addToken(output, 'w', match[0]);
                pos += match[0].length;
                continue;
            }

            // Newlines
            if (source[pos] === '\n') {
                addToken(output, 'w', '\n');
                pos++;
                continue;
            }

            // Ordinary text
            match = rest.match(/^[^\s,;:|!={}/]+/);

            if (match) {
                addToken(output, '', match[0]);
                pos += match[0].length;
                continue;
            }

            // Remaining characters, including standalone slashes
            addToken(output, '', source[pos]);
            pos++;
        }

        return output;
    }

    /** Find and highlight code blocks */
    function processZedScripts(content) {
        let roots;

        if (content && content.jquery) {
            roots = content.toArray();
        } else {
            roots = [content];
        }

        roots.forEach(function (root) {
            if (!root || !root.querySelectorAll) {
                return;
            }

            const blocks = [];

            if (
                root.matches &&
                root.matches('.zedscripts pre')
            ) {
                blocks.push(root);
            }

            root.querySelectorAll('.zedscripts pre')
                .forEach(function (pre) {
                    blocks.push(pre);
                });

            blocks.forEach(function (pre) {
                if (pre.dataset.zedscriptsHighlighted === 'true') {
                    return;
                }

                const source = pre.textContent;

                pre.replaceChildren(
                    highlightZedScripts(source)
                );

                pre.dataset.zedscriptsHighlighted = 'true';
            });
        });
    }

    /** Initialise */

    // Process the current page
    processZedScripts(document);

    // Process content loaded dynamically by MediaWiki
    mw.hook('wikipage.content').add(function (content) {
        processZedScripts(content);
    });

})();
