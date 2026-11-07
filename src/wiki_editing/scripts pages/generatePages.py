import yaml, os, json, re
from pprint import pprint

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.join(SCRIPT_PATH, '..', '..')
SCRIPT_BLOCK_PATH = os.path.join(PROJECT_PATH, 'pz-scripts-data', 'data', 'blocks')
OUTPUT_PATH = os.path.join(PROJECT_PATH, 'Drafts', 'Scripts', 'Parameters')

class Template:
    _cached = {}

    PATH = os.path.join(SCRIPT_PATH, 'templates')    
    FORMAT_REGEX = re.compile(r'\$\$(\w+)\$\$')

    # template pages
    MAIN = "MAIN.wt"
    EXAMPLE = "EXAMPLE.wt"
    END = "END.wt"

    @staticmethod
    def get_content(template_name, values={}):
        if template_name in Template._cached:
            page = Template._cached[template_name]
        else:
            with open(os.path.join(Template.PATH, template_name), 'r', encoding='utf-8') as f:
                page = f.read()
                Template._cached[template_name] = page
        page_formatted = Template.FORMAT_REGEX.sub(lambda m: values[m.group(1)], page)
        return page_formatted

class DefaultText:
    PAGENAME = '{param_name} ({block_name} parameter)'
    FILENAME = '{page_name}.wt'
    CATEGORY = '{block_name} parameters'
    DESCRIPTION = '{{Code|{param_name}}} is a parameter of the {{Code|{block_name}}} script block.'


# list blocks
blocks = {}
for block_file in os.listdir(SCRIPT_BLOCK_PATH):
    if block_file.endswith('.yaml'):
        block_name = block_file[:-5]
        with open(os.path.join(SCRIPT_BLOCK_PATH, block_file), 'r') as f:
            block_data = yaml.safe_load(f)
            blocks[block_name] = block_data


for block_name, block_data in blocks.items():
    parameters = block_data.get('parameters', [])
    print(block_name, len(parameters))
    for param_data in parameters:
        param_name = param_data['name']
        param_desc = param_data.get(
            'description', 
            DefaultText.DESCRIPTION.format(param_name=param_name, block_name=block_name)
        )

        # if param_desc is None:
        #     continue
        
        page_name = DefaultText.PAGENAME.format(param_name=param_name, block_name=block_name)
        # print(page_name)
        filename = DefaultText.FILENAME.format(page_name=page_name)
        output_file_path = os.path.join(OUTPUT_PATH, 'auto', block_name, filename)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            values = {
                'PAGENAME': page_name,
                'PARAM_NAME': param_name,
                'BLOCK_NAME': block_name,
                'PARAM_DESC': param_desc,
                'CATEGORY': DefaultText.CATEGORY.format(block_name=block_name),
                # 'example_code': param_data.get('example', None),
            }

            # top section
            content = Template.get_content(Template.MAIN, values)
            f.write(content)

            # # example section
            # if values['example_code'] is not None:
            #     content = Template.get_content(Template.EXAMPLE, values)
            #     f.write(content)
                
            # end section
            content = Template.get_content(Template.END, values)
            f.write(content)
