import os, yaml, pyperclip, json

DATA_PATH = os.path.join("pz-translation-data", "data")
TRANSLATION_DATA_PATH = os.path.join(DATA_PATH, "translationFiles.json")

with open(TRANSLATION_DATA_PATH, "r") as f:
    translation_data = json.load(f)

translation_list = []
for translation_type, data in translation_data.items():
    translation_list.append((translation_type, data))

translation_list.sort(key=lambda x: x[0])

txt = ""
for translation_type, data in translation_list:
    keyPrefix = data.get("keyPrefix", None)
    if keyPrefix is not None:
        keyPrefix = f"<code>{keyPrefix}</code>"
    else:
        keyPrefix = ""

    function = data.get("function", None)
    if function is not None:
        function = f"<code>{function}</code>"
    else:
        function = ""

    filename = data.get("fileName", None)
    if filename is not None:
        filename = f"<code>{filename}</code>"
    else:
        filename = ""

    description = data.get("description", "")

    txt += f"|-\n| {translation_type} || {filename} || {keyPrefix} || {function} ||\n{description}\n"

pyperclip.copy(txt)
print(txt)