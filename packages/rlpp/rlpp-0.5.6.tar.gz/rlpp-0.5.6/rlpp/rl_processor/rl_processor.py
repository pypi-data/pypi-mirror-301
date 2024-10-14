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

    object_lists = read_json_file(path) #parse the json data
    tab = "    " #the txt template has a specific number of spaces for tabs
    text_for_static = "" #some objects are not remade at the beginning of the game, like agents and enemies
    text_for_dynamic = "" #food and walls are remade at the beginning of the game
    list_collection_static = [] #contain the name of the list with static game objects
    list_collection_dynamic = [] #contain the name of the list with the dynamic game objects
    
    ########## HANDLE GAME OBJECTS #################
    # each key represents a : wall, agent, enemies, foods
    # For each key:
    #   determine if it's static or dynamic
    #   create a new line declaring a new list with the name of the 
    for key in object_lists.keys():
        # static objects
        if "agent" in key or "enem" in key:
            goes_to_static = True
            _str = f"{tab}{tab}self.{key}=[]\n"             #create list name (e.g. self.agents = [])
            list_collection_static.append(f"self.{key}")           #add list name to the collection (all game objects are part of the same master list) that are static
        # dynamic objects
        else:
            goes_to_static = False    
            _str = f"{tab}{tab}self.{key}=[]\n"             #create list name (e.g. self.agents = [])
            list_collection_dynamic.append(f"self.{key}")           #add list name to the collection (all game objects are part of the same master list) that are dynamic
            
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
        
        
        if goes_to_static:
            text_for_static += _str
        else:
            text_for_dynamic += _str
    text_for_static += f'{tab}{tab}self.static_game_objects = [{",".join(list_collection_static)}]\n'
    text_for_dynamic += f'{tab}{tab}self.all_game_objects = self.static_game_objects + [{",".join(list_collection_dynamic)}]\n'
            
    #################################################################
    template_location = jn(os.path.dirname(__file__),"template_gameManager.txt")
    with open(template_location,'r') as file:
        file = file.read()
    
    with open(jn(os.path.split(path)[0],"rl_output.py"),"w") as py_file:
        file = file.replace("<<embed_static_game_objects>>",text_for_static)
        file = file.replace("<<embed_dynamic_game_objects>>",text_for_dynamic)
        py_file.write(file)
    
    model_template_location = jn(os.path.dirname(__file__),"template_model.txt")
    with open(model_template_location,"r") as file:
        template_model_string = file.read()
    
    with open(jn(os.path.split(path)[0],"Model.py"),"w") as model_py_file:
        model_py_file.write(template_model_string)
    
# map_json(r"C:\Users\Uriel\Desktop\test.json")