import json

file = "/home/simon/Documents/Repositories/pz-wiki_parser/data/item_data.json"

cmd = input("Command: ")

if cmd == "1":
    unique = {}
    with open(file, "r") as f:
        data = json.load(f)
        for item in data.values():
            if "Type" in item:
                unique[item["Type"]] = item

    s = "*{{{{JavaObject|{0}|package=zombie/inventory/types|customDoc=https://demiurgequantified.github.io/ProjectZomboidJavaDocs/}}}}"
    for k, v in unique.items():
        print(s.format(k))

    print()
    for k, v in unique.items():
        print("*" + k)

elif cmd == "2":
    classes = {}
    unique_params = []
    with open(file, "r") as f:
        data = json.load(f)
        for fullType, item in data.items():
            if type(item) is not dict:
                continue
            for k, v in item.items():
                if k not in unique_params:
                    unique_params.append(k)

                if "Type" not in item:
                    print(fullType, "no type found")

                Type = item["Type"]
                if Type not in classes:
                    classes[Type] = []

                if k not in classes[Type]:
                    classes[Type].append(k)

    unique_params.sort()

    uniques_classes = list(classes.keys())
    uniques_classes.sort()

    # simple print
    for k, v in classes.items():
        print("*" + k)
        for field in v:
            print("**" + field)
        print()

    symbol = {
        "present": "[[File:UI Tick.png]]",
        "absent": "",
    }

    header = (
        """{| class="wikitable theme-blue sortable mw-collapsible mw-collapsed" style="text-align: center;\n"""
        + """|+ style="white-space:nowrap" | Parameters used by the vanilla game for the various item classes\n"""
        + """|-\n"""
    )
    types_row = "! Parameter !! " + " !! ".join(uniques_classes) + "\n"


    # write to file wiki table
    with open("output.wt", "w") as f:
        f.write("==Parameters comparison==\n")
        f.write(header)
        f.write(types_row)
        for param in unique_params:
            row = "|-\n| " + param + " || "
            row += " || ".join(
                symbol["present"] if param in classes[c] else symbol["absent"]
                for c in uniques_classes
            )
            row += "\n"
            f.write(row)
        f.write("|}")
    f.close()