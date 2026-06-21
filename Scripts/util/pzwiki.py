import re


def mediawiki_to_pzwiki(text: str) -> str:
    """
    Convert MediaWiki markup to PZWiki markup:
    - <syntaxhighlight> to {{CodeSnip|lang=...|code=...}}
    - `[https://pzwiki.net/wiki/<page> text]` to `[[<page>|text]]`
    """
    # Convert <syntaxhighlight> to {{CodeSnip|lang=...|code=...}}
    text = re.sub(
        r"\n?<syntaxhighlight lang=\"(.*?)\">(.*?)</syntaxhighlight>",
        r"{{CodeSnip\n| lang = \1\n| code = \n\2\n}}\n",
        text,
        flags=re.DOTALL,
    )

    # Convert `[https://pzwiki.net/wiki/<page> text]` to `[[<page>|text]]`
    text = re.sub(
        r"\[https://pzwiki\.net/wiki/(.*?) (.*?)\]",
        r"[[\1|\2]]",
        text,
        flags=re.DOTALL,
    )
    return text