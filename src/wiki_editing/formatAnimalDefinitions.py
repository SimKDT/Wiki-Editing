import re, yaml
from pprint import pprint

CONSOLE_FILE = "/home/simon/Zomboid/console.txt"



with open(CONSOLE_FILE, "r", encoding="utf-8") as f:
    data = f.read()

    # Extract only the text between the fetch start and end indications
    start_marker = 'FETCHING AnimalDefinitions DATA'
    end_marker = 'END FETCHING'

    start_idx = data.find(start_marker)
    end_idx = data.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        # Include the start marker line, exclude the end marker line
        start_idx = data.find('\n', start_idx) + 1  # move to line after start_marker
        data = data[start_idx:end_idx].strip()
    else:
        data = ""

    # remove first line
    data = '\n'.join(data.splitlines()[1:])

    # remove two last lines
    data = '\n'.join(data.splitlines()[:-2])


# Remove the specified text using regex
data = re.sub(r'LOG  : General\s+f:0, t:\d+>', '', data)
data = '\n'.join(line[1:] for line in data.splitlines())

# print(data)

OUTPUT_FILE = "./Data/AnimalDefinitions.yaml"
# with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#     f.write(data)

# read the file
with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)


# # list genes
# uniques = {}
# for animal, details in data["genome"].items():
#     for gene in details["genes"]:
#         if gene not in uniques:
#             uniques[gene] = True

# for gene in uniques.keys():
#     print(gene)

# # list breed parameters
# uniques = {}
# for details in data["breeds"].values():
#     for details2 in details.values():
#         for details3 in details2.values():
#             for param in details3.keys():
#                 if param not in uniques:
#                     uniques[param] = True

# for param in uniques.keys():
#     print(param)

# list animal def parameters
uniques = {}
for details in data["animals"].values():
    for param in details.keys():
        if param not in uniques:
            uniques[param] = True

for param in uniques.keys():
    print(param)