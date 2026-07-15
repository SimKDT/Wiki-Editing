import json
import xml.etree.ElementTree as ET
from pathlib import Path



INPUT_XML = Path("Old/item_parameters.xml")
OUTPUT_DIR = Path("Old/item_parameters")

ns = {
    'mediawiki': r"http://www.mediawiki.org/xml/export-0.11/",
}

# read the XML
tree = ET.parse(INPUT_XML)
root = tree.getroot()

out = {}

for page in root.findall('mediawiki:page', ns):
    title_element = page.find('mediawiki:title', ns)
    if title_element is None:
        print("No title found for a page, skipping.")
        continue
    title = title_element.text
    if title is None:
        print("Title is None for a page, skipping.")
        continue

    # clear title of any () text, e.g., "Icon (item parameter)" becomes "Icon"
    title = title.split('(')[0].strip()
    output_file = (OUTPUT_DIR / f"{title}.wt")
    out[title] = str(output_file)
    
    try:
        text_element = page.find('mediawiki:revision/mediawiki:text', ns)
        if text_element is None:
            print(f"No text found for page: {title}, skipping.")
            continue
        text = text_element.text
        if text is None:
            print(f"Text is None for page: {title}, skipping.")
            continue

        # create a file for each page
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Error processing page: {title}. Error: {e}")

with open(INPUT_XML.parent / (INPUT_XML.stem + ".json"), "w") as f:
    json.dump(out, f, indent=4)