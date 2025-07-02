import os, json
from typing import List
import requests
from pathlib import Path


loop = ""
start = ""
name_cheat = ""
path = ""


def loadstring(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        code = response.text
        exec(code, globals())  # executa o código no escopo global
    else:
        raise Exception(f"Err: {response.status_code}")

def add_cmd(type:str, cmd:str):
    global start, loop  # adiciona isso para alterar as variáveis globais
    
    if type == "start":
        start = start + f"\n{cmd}"
    elif type == "loop":
        loop = loop + f"\n{cmd}"

def cmd(cmd:str, type: str):
    if type == "start":
        add_cmd("start", cmd)
    elif type == "loop":
        add_cmd("loop", cmd)

def inject(p: str):

    data = name_cheat.lower()

    base_path = os.path.join(p, data)
    functions_path = os.path.join(base_path, 'data', data, 'function')
    tags_path = os.path.join(base_path, 'data', 'minecraft', 'tags', 'function')

    # Cria as pastas necessárias
    os.makedirs(functions_path, exist_ok=True)
    os.makedirs(tags_path, exist_ok=True)

    # Cria pack.mcmeta
    pack_mcmeta = {
        "pack": {
            "pack_format": 81,  # ajustar conforme versão do Minecraft
            "description": f"Datapack {data}",
            "script": True
        }
    }
    with open(os.path.join(base_path, 'pack.mcmeta'), 'w', encoding='utf-8') as f:
        json.dump(pack_mcmeta, f, indent=4)

    # Escreve os comandos start.mcfunction
    with open(os.path.join(functions_path, 'load.mcfunction'), 'w', encoding='utf-8') as f:
        f.write(start.strip() + '\n')  # tira linhas extras no começo/fim e adiciona \n no fim

    # Escreve os comandos loop.mcfunction
    with open(os.path.join(functions_path, 'tick.mcfunction'), 'w', encoding='utf-8') as f:
        f.write(loop.strip() + '\n')

    # Cria load.json
    load_json = {
        "values": [f"{data}:load"]
    }
    with open(os.path.join(tags_path, 'load.json'), 'w', encoding='utf-8') as f:
        json.dump(load_json, f, indent=4)

    # Cria tick.json
    tick_json = {
        "values": [f"{data}:tick"]
    }
    with open(os.path.join(tags_path, 'tick.json'), 'w', encoding='utf-8') as f:
        json.dump(tick_json, f, indent=4)

    print(f"Datapack '{data}' path '{p}'.")

def give(_entity: str, item: str, NBT: str, count: int, _type: str):
    cmd(f"give {_entity} {item}[{NBT}] {count}", _type)

def teleport(_entity: str, _vector3: List[float], angle: List[float], _type: str):
    if angle == [0, 0, 0]:
        cmd(f"tp {_entity} {_vector3[0]} {_vector3[1]} {_vector3[2]}", _type)
    else:
        if _vector3 == [0, 0, 0, 0]:
            cmd(f"tp {_entity} ~ ~ ~ {angle[0]} {angle[1]}", _type)
        else:
            cmd(f"tp {_entity} {_vector3[0]} {_vector3[1]} {_vector3[2]} {angle[0]} {angle[1]}", _type)

def Vector3(x: float, y: float, z: float):
    return [x, y, z]

def Vector3_normal():
    return [0, 0, 0, 0]

def angle(horizontal: float, vertical: float):
    return [horizontal, vertical]

class direction():

    @staticmethod
    def east():
        return [-90, 0]
    
    @staticmethod
    def north():
        return [-180, 0]
    
    @staticmethod
    def west():
        return [90, 0]
    
    @staticmethod
    def south():
        return [0, 0]
    
    @staticmethod
    def normal():
        return [0, 0, 0]
#east = -90, 0, north = -180, 0, west = 90, 0, south = 0, 0
class Entity:
    @staticmethod
    def player(ply: str):
        return ply

    @staticmethod
    def entity(mb: str):
        return f"@e[type={mb}]"

    @staticmethod
    def all_players():
        return "@a"

    @staticmethod
    def closest_player():
        return "@p"

    @staticmethod
    def all_entity():
        return "@e"

class Type:

    @staticmethod
    def loop():
        return "loop"
    
    @staticmethod
    def start():
        return "start"

def clear():
    global loop, start
    loop = ""
    start = ""

def name(_name: str):
    global name_cheat
    name_cheat = _name

def summon(_entity: str, _vector3: List[float], NBT: str, _type: str):
    cmd(f"summon {_entity} {_vector3[0]} {_vector3[1]} {_vector3[2]} {{{NBT}}}", _type)

class scoreboards():
    
    @staticmethod
    def create_(id: str, _type: str, display_name: str, _type_: str):
        cmd(f"scoreboard objectives add {id} {_type} \"{display_name}\"", _type_)

    @staticmethod
    def create(id: str, _type: str, _type_: str):
        cmd(f"scoreboard objectives add {id} {_type}", _type_)

    @staticmethod
    def set(_entity: str, id: str, value: float, _type_: str):
        cmd(f"scoreboard players set {_entity} {id} {value}", _type_)

    @staticmethod
    def add(_entity: str, id: str, value: float, _type_: str):
        cmd(f"scoreboard players add {_entity} {id} {value}", _type_)

    @staticmethod
    def remove(_entity: str, id: str, value: float, _type_: str):
        cmd(f"scoreboard players remove {_entity} {id} {value}", _type_)

    @staticmethod
    def show(_type: str, id: str, _type_: str):
        cmd(f"scoreboard objectives setdisplay {_type} {id}", _type_)

    def delete(id: str, _type: str):
        cmd(f"scoreboard objectives remove {id}", _type)

def execute(conditions: list, run: str, _type: str):
    ce = " ".join(conditions)
    cmd(f"execute {ce} run {run}", _type)

def extra_inject():

    _path_ = Path(__file__).resolve()
    _path_ = _path_.parent.parent

    with open(f"{_path_}\\config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    path = config["path"]

    inject(f"{path}\\datapacks")
