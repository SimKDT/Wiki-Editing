import json, re
from pathlib import Path

## PARAMETERS

PAGES_JSON = Path("Old/item_parameters.json")
OUTPUT_DIR = Path("Old/to_outdated/item_parameters")

OUTDATED_TEXT = r"""
{{Deletion|This parameter page is deprecated. Please refer to the [[PZ API Documentation|ScriptsDocs]] for the most up-to-date information.
""".strip()

ADD_AFTER = r"{{Page version[\S\s]+?}}"



# link to other docs
registry = {
    "ItemTag": "Tags",
}


ITEM_BLOCK_LINK = r"https://pz-wiki-modding.github.io/PZ-API-Docs/scripts/item.html"
SCRIPTS_DATA = Path("pz-scripts-data/out/scriptBlocks.json")
with open(SCRIPTS_DATA, "r", encoding="utf-8") as f:
    script_blocks = json.load(f)

def format(id, outdated_text):
    item_block = script_blocks['item']
    parameters = item_block['parameters']

    isParam = id.lower() in parameters.keys()

    if not isParam:
        if id in registry:
            isParam = True
            id = registry[id]
        else:
            print(f"Parameter '{id}' not found in script blocks.")
            outdated_text += " This parameter is not documented in the ScriptsDocs, meaning it is either yet documented or non-existent in [[Build 42]]."

    if isParam:
        params = {
            "$LINK": f"{ITEM_BLOCK_LINK}#{id.lower()}"
        }

        new_link_paragraph = r"You can find the ScriptsDocs entry for this parameter [$LINK here]."

        for key, value in params.items():
            outdated_text += " " + new_link_paragraph.replace(key, value)

    outdated_text += "}}"

    return outdated_text






## UTILITY

def add_outdated_block(id, content, outdated_text):
    match = re.search(ADD_AFTER, content)
    if match:
        end = match.end()
        return content[:end] + "\n" + outdated_text + content[end:]
    else:
        print(f"Warning: pattern not found in content for id '{id}'.")
        return outdated_text + "\n" + content




## MAIN

with open(PAGES_JSON, "r", encoding="utf-8") as f:
    pages = json.load(f)

for id, path in pages.items():
    input_file = Path(path)
    if not input_file.exists():
        print(f"Input file does not exist: {input_file}")
        continue

    output_file = OUTPUT_DIR / input_file.name
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # specific parameters
    outdated_text = format(id, OUTDATED_TEXT)

    # add a header with outdated block
    content = add_outdated_block(id, content, outdated_text)


    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

