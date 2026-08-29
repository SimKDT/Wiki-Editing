from pathlib import Path

from util.execute_lua import run_files


lua_files: list[Path] = []

for lua_file in Path("/home/simon/.steam/debian-installation/steamapps/common/ProjectZomboid/projectzomboid/media/lua/client/DebugUIs/Scenarios").glob("*.lua"):
    lua_files.append(lua_file)

from pprint import pprint
pprint(lua_files)

lua, modules = run_files(lua_files)
scenarios = lua.globals().debugScenarios

names = {key: data.name for key, data in scenarios.items()}
names_list = sorted(names.values())

for name in names_list:
    print(f"* {name}")