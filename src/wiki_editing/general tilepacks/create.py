import json, os
from string import Template

PATHS = {
    'tilepacks': 'tilepacks.json',
    'template': 'TEMPLATE.wt',
}

script_path = os.path.dirname(os.path.abspath(__file__))

for key, path in PATHS.items():
    PATHS[key] = os.path.join(script_path, path)

with open(PATHS['tilepacks'], 'r') as file:
    data = json.load(file)

template_path = PATHS['template']
with open(template_path, 'r', encoding='utf-8') as template_file:
    template_content = template_file.read()
    TEMPLATE = Template(template_content)

class IMAGE_TYPES:
    THUMBNAIL = 'thumbnail'
    PREVIEW = 'preview'

class Tilepack:
    params = {}
    DEFAULT_NAME = "Tile pack ({NAME})"
    DEFAULT_EXTENSION = 'jpeg'
    DEFAULT_GALLERY = '{{Clear}}'
    GALLERY_TEMPLATE = "\n== Gallery ==\n<gallery>\n{files}\n</gallery>\n"
    THUMBNAIL_TEMPLATE = "{NAME} - thumbnail.{EXT}"

    def __init__(self, entry):
        params = {
            'NAME': self.DEFAULT_NAME.format(NAME=entry['NAME']),
            'WORKSHOPID': entry['WORKSHOPID'],
            'VERSION': entry['VERSION'],
            'GALLERY': self.DEFAULT_GALLERY,
        }
        print("GENERATING: " + params['NAME'])
        self.params = params
        self.get_images(entry.get('IMAGE_FILES', {}))

    def get_images(self, image_definitions):
        images = []
    
        # get thumbnail
        if IMAGE_TYPES.THUMBNAIL in image_definitions:
            thumbnail = image_definitions[IMAGE_TYPES.THUMBNAIL]
            ext = self.get_extension(thumbnail)
            file_name = self.THUMBNAIL_TEMPLATE.format(NAME=self.params['NAME'], EXT=ext)
            images.append(file_name)

        if IMAGE_TYPES.PREVIEW in image_definitions:
            previews = image_definitions[IMAGE_TYPES.PREVIEW]
            preview_count = previews.get("count", 0)
            assert preview_count > 0, "Preview count must be greater than 0"
            if preview_count > 1:
                gallery = []
                for i in range(1, preview_count + 1):
                    ext = self.get_extension(previews)
                    file_name = f"File:{self.params['NAME']} - preview{i}.{ext}"
                    gallery.append(file_name)
                gallery_str = "\n".join(gallery)
                self.params['GALLERY'] = self.GALLERY_TEMPLATE.format(files=gallery_str)
            else:
                ext = self.get_extension(previews)
                file_name = f"{self.params['NAME']} - preview.{ext}"
                images.append(file_name)

        if len(images) > 0:
            images_str = "\n    {{Infobox/image\n"
            for idx, img in enumerate(images):
                images_str += f"    | p{idx + 1} = [[File:{img}]]\n"
            for idx, img in enumerate(images):
                images_str += f"    | {idx + 1} = [[File:{img}|link=]]\n"
            images_str += "    }}\n"
            self.params['IMAGES'] = images_str
        else:
            self.params['IMAGES'] = ""

    def get_extension(self, thumbnail):
        if type(thumbnail) is dict:
            return thumbnail.get('EXT', self.DEFAULT_EXTENSION)
        return self.DEFAULT_EXTENSION
    
    def create(self):
        return TEMPLATE.substitute(**self.params)

if __name__ == "__main__":
    for entry in data:
        tilepack = Tilepack(entry)
        content = tilepack.create()
        file_name = f"{tilepack.params['NAME']}.wt"
        path = os.path.join(script_path, "pages", file_name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as output_file:
            output_file.write(content)