
/* ============================================================
   ZedScripts syntax highlighting
   Usage: 
   <syntaxhighlight lang="text" class="zedscripts">
   item ID {
     param1 = value1,
   }
   </syntaxhighlight>
   ============================================================ */

(function () {
    'use strict';

    // --------------------------------------------------------
    // Token creation
    // --------------------------------------------------------

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

    // --------------------------------------------------------
    // ZedScripts lexer
    // --------------------------------------------------------

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

    // --------------------------------------------------------
    // Find and highlight code blocks
    // --------------------------------------------------------

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

    // --------------------------------------------------------
    // Initialise
    // --------------------------------------------------------

    // Process the current page
    processZedScripts(document);

    // Process content loaded dynamically by MediaWiki
    mw.hook('wikipage.content').add(function (content) {
        processZedScripts(content);
    });

})();
