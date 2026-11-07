import json

parser_path = "/home/simon/Documents/Repositories/pz-wiki_parser/data/cache/parsed_entity_data.json"

with open(parser_path, "r") as f:
    data = json.load(f)

components = {}
for entity_type, entity_data in data.items():
    if type(entity_data) is not dict:
        continue
    for component_type, component_data in entity_data.items():
        if type(component_data) is not dict:
            if component_type not in components:
                components[component_type] = True
        else:
            if component_type not in components:
                components[component_type] = set()
            for field in component_data.keys():
                components[component_type].add(field)


## print components
for component_type, fields in components.items():
    print("* " + component_type)
    if fields is True:
        continue
    else:
        for field in sorted(fields):
            print("    ** " + field)
