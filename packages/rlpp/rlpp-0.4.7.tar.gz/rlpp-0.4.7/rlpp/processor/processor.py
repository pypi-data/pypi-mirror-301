import pygame 
import os 
import json 
from os.path import join as jn
"""Read a config.json file and map it into a pygame.py file"""

def map_json(path):
    def read_json_file(file_path):
        # Open the JSON file and load its contents
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    object_lists = read_json_file(path)
    text_for_template = ""
    tab = "    "
    list_collection = [] #at the end, all lists will be nested within a main list_of_game_objects
    # each key represents a list
    for key in object_lists.keys():
        _str = f"{tab}{tab}self.{key}=[]\n"             #create list name (e.g. self.agents = [])
        list_collection.append(f"self.{key}")           #add list name to the collection (all game objects are part of the same master list)
        # create the game object that corresponds to the json file elements
        for idx,go in enumerate(object_lists[key]):
            # case 1: agents
            if "agent" in key:
                _str += f"{tab}{tab}self.go_agent_{idx} = Agent({go['position']},{go['angle']},\"{go['object_type']}\",r\"{go['img_path']}\",abs({round(go['scale_factor'],4)}));self.{key}.append(self.go_agent_{idx})\n"
            # case 2: walls
            if "wall" in key:
                _str += f"{tab}{tab}self.go_wall_{idx} = Wall({go['position']},{go['angle']},\"{go['object_type']}\",r\"{go['img_path']}\",abs({round(go['scale_factor'],4)}));self.{key}.append(self.go_wall_{idx})\n"
            # case 1: enemies
            if "enem" in key:
                _str += f"{tab}{tab}self.go_enemy_{idx} = Enemy({go['position']},{go['angle']},\"{go['object_type']}\",r\"{go['img_path']}\",abs({round(go['scale_factor'],4)}));self.{key}.append(self.go_enemy_{idx})\n"
            # case 1: foods
            if "food" in key:
                _str += f"{tab}{tab}self.go_food_{idx} = Food({go['position']},{go['angle']},\"{go['object_type']}\",r\"{go['img_path']}\",abs({round(go['scale_factor'],4)}));self.{key}.append(self.go_food_{idx})\n"
            
        text_for_template += _str
    text_for_template += f'{tab}{tab}self.all_game_objects = ({",".join(list_collection)})\n'
    
    template_location = jn(os.path.dirname(__file__),"template.txt")
    with open(template_location,'r') as file:
        file = file.read()
    
    with open(jn(os.path.split(path)[0],"output.py"),"w") as py_file:
        file = file.replace("<<embed_game_objects>>",text_for_template)
        py_file.write(file)
    
# map_json(r"C:\Users\Uriel\Desktop\test.json")