import pygame 
import numpy as np 
from PyQt5.QtGui import QImage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, QFileDialog,QMessageBox,QShortcut
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QKeySequence
import os
from os.path import join as jn
import cv2
import sys
import json 
import random

RES = 32 #resolution of reference from the resouces folder
dir_location = str(os.path.dirname(__file__))
RESOURCES_PATH = jn(dir_location,"resources",f"res_{RES}")
ICONS_PATH = jn(dir_location,"resources","icons")
# background_path = jn(dir_location,"resources","backgrounds","bg_map.png")
# print(background_path)
SCREEN = (640,480)
pygame_surface = pygame.Surface(SCREEN)  # Pygame rendering surface)

# cursor settings
cursor_settings = {"POS":(0,0),"MODE":"", "INDISPLAY":False, "RESIZESENS":0.1}


# DD. GAME_OBJECT
# gameObject = GameObject()
# interp. a game object in the editor with:
# - position x and y in the screen, where coordinate is the center of the object
# - image loaded in pygame
# - object_type: agent, wall, enemy, food
class GameObject():
    def __init__(self,object_type, img_path):
        self.placed = False #stops following cursor once it's placed
        self.object_type = object_type
        self.image_path = img_path
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.angle = 0
        self.scaleFactor = 1

        
    def draw(self):
        pygame_surface.blit(self.image, self.rect)
        if self == objectManager.current_go:
            pygame.draw.rect(pygame_surface,"green",self.rect,1)
        
    def update_pos(self):
        if not self.placed:
            self.rect.center = cursor_settings["POS"]

    def turnClockwise(self, degrees=90):
        # Preserve the current center position of the rectangle
        self.angle = (self.angle + degrees)%360
        previous_center = tuple(self.rect.center)
        # Rotate the image
        self.image = pygame.transform.rotate(self.image, -degrees)  # Use -self.angle for clockwise rotation
        self.rect = self.image.get_rect(center=previous_center)  # Reassign the rect with the updated center
    
    def scale(self,val):
        self.scaleFactor += val
        w,h = self.image.get_size()
        previous_center = tuple(self.rect.center)
        new_size = (int(w * (1+val)), int(h * (1+val)))
        
        is_size_over_512 = new_size[0] > 512 and new_size[1] > 512
        is_size_under_10 = new_size[0] < 10 and new_size[1] < 10
        
        # size > 512:
        #   val > 0: not allowed
        #   val < 0: allowed
        # size < 512:
        #   val < 0 and not size < 10: allowed
        #   both allowed
        
        
        # size under 10:
        
        # size not over 512 and user wants to increase size
        if (is_size_over_512 and val<0) or (is_size_under_10 and val>0) or (not is_size_over_512 and not is_size_under_10):
            self.image = pygame.transform.scale(self.image, new_size)
            self.rect = self.image.get_rect(center=previous_center)  # Reassign the rect with the updated center
        
            
    def to_dict(self):
        d = {"position":self.rect.center,
             "angle":self.angle,
             "img_path":self.image_path,
             "object_type":self.object_type,
             "scale_factor":self.scaleFactor
             }
        return d
        
# Objects display manager allows mainUI and main to access the collection of objects that are being placed within the screen
# DD. DesignerObjectManager()
# gm = DesignerObjectManager()
# interp. an object to track the parameters and objects placed in the designer by the player
class DesignerObjectManager():
    def __init__(self):
        self.walls = []
        self.agents = []
        self.foods = []
        self.enemies = []
        self.list_names = ["walls","agents","foods","enemies"]
        self.gameObjects = [self.walls ,self.agents ,self.foods ,self.enemies]
        self.current_go = None
        
    def updateGameObjects(self):
        for logo in self.gameObjects:
            for go in logo:
                go.draw()
    
    
    def update_pygame(self, qlabel):
        # Render Pygame content (for example, a red circle moving across the screen)
        pygame_surface.fill((30, 30, 30))  # Clear screen
        # UPDATE THE GAMEOBJECTS IN THE MANAGER
        self.updateGameObjects()
        if self.current_go is not None:
            self.current_go.update_pos()
            self.current_go.draw()
        
        # pygame.draw.circle(pygame_surface, (255, 0, 0), cursor_settings["POS"], 50)
        # Convert Pygame surface to an image that PyQt can display
        self.display_pygame_on_qt(qlabel)

    def display_pygame_on_qt(self, qlabel):
        # Get the Pygame surface as a 3D array (RGB format)
        raw_image = pygame.surfarray.array3d(pygame_surface)
        # Convert from (width, height, color) to (height, width, color)
        raw_image = np.transpose(raw_image, (1, 0, 2))

        # Convert the image to a format suitable for PyQt5 (QImage)
        height, width, channel = raw_image.shape
        bytes_per_line = 3 * width
        qt_image = QImage(raw_image.tobytes(), width, height, bytes_per_line, QImage.Format_RGB888)

        # Set the QPixmap to the QLabel to display it
        qlabel.setPixmap(QPixmap.fromImage(qt_image))
    
    def create_new_gameObject(self,img_path,object_type, reset_mode=False):
        cursor_settings["MODE"] = "" if reset_mode else cursor_settings["MODE"]
        if object_type == "agent":
            gameObject = GameObject("agent",img_path)
            self.current_go = gameObject
            # self.agents.append(gameObject)
        elif object_type == "wall":
            gameObject = GameObject("wall",img_path)
            self.current_go = gameObject
            # self.walls.append(gameObject)
        elif object_type == "enemy":
            gameObject = GameObject("enemy",img_path)
            self.current_go = gameObject
            # self.enemies.append(gameObject)
        elif object_type == "food":
            gameObject = GameObject("food",img_path)
            self.current_go = gameObject
            # self.foods.append(gameObject)
            
    def processCurrentObject(self):
        if self.current_go.object_type == "agent":
            self.agents.append(self.current_go)
        elif self.current_go.object_type == "wall":
            self.walls.append(self.current_go)
        elif self.current_go.object_type == "enemy":
            self.enemies.append(self.current_go)
        elif self.current_go.object_type == "food":
            self.foods.append(self.current_go)
        self.current_go.placed = True
        
        # Control the behavior of the STAMP tool
        if not cursor_settings["MODE"] == "STAMP":
            self.current_go = None
        else:
            angle_reference = self.current_go.angle
            self.create_new_gameObject(self.current_go.image_path,self.current_go.object_type)
            self.current_go.turnClockwise(angle_reference)
        
    def getObjectClicked(self):
        '''Iterate over all the elements in the game to find that which overlaps the cursor '''
        for logo in self.gameObjects:
            for go in logo:
                if go.rect.collidepoint(cursor_settings["POS"]):
                    self.current_go = go 
                    return
        # if no object was clicked, set to current_go to None
        self.current_go = None
            
    def remove_current_gameObject(self):
        for logo in self.gameObjects:
            for go in logo:
                if go == self.current_go:
                    self.current_go = None
                    cursor_settings["MODE"] = "SELECT"
                    logo.remove(go)
                    return 
    
    def export_JSON(self):
        config = {list_name:[go.to_dict() for go in self.gameObjects[idx]] for idx, list_name in enumerate(self.list_names)}
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None, "Save File", "config.json", "JSON Files (*.json);;All Files (*)", options=options)
                
        if fileName:
            filename_root = os.path.split(fileName)[0]
            new_images_path = jn(filename_root,"images")
            # make the images directory if it doesn't exist yet
            if not os.path.exists(new_images_path):
                os.mkdir(new_images_path)
                
            # extract unique records of image paths
            images_locations = []
            for logo in self.gameObjects:
                for go in logo:
                    if go.image_path not in images_locations:
                        images_locations.append(go.image_path)
            
            # save a copy of the each image in the folder images
            for image_path in images_locations:
                im = cv2.imread(image_path,cv2.IMREAD_UNCHANGED)
                # split the name of the image from its root
                image_name = os.path.split(image_path)[1]
                # save the image in the new path
                _new_im_path = jn(new_images_path,image_name)
                cv2.imwrite(_new_im_path, im)
                # change the game objects with the previous image_path to the new _new_im_path located where the config.json file is
                for logo in self.gameObjects:
                    for go in logo:
                        if go.image_path == image_path:
                            go.image_path = _new_im_path
            
            config = {list_name:[go.to_dict() for go in self.gameObjects[idx]] for idx, list_name in enumerate(self.list_names)}
            if not fileName.endswith('.json'):
                fileName += '.json'
            with open(f"{fileName}","w") as jsonfile:
                json.dump(config, jsonfile, indent=4)  # Use json.dump to write the dictionary to the file
            QMessageBox.information(None, "File Selected", f"File will be saved as: {fileName}")

    # determine whether the current game object has already been placed
    def current_go_in_collections(self):
        for logo in self.gameObjects:
            for go in logo:
                if self.current_go == go:
                    return True 
        return False
    
objectManager = DesignerObjectManager()