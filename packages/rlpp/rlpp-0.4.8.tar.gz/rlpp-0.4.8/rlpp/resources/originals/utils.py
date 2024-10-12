# A suite of tools to manage sprite's resolution
# purp. create a new folder with the image of each sprite scaled at the desired resolution


# Modules
import os
from os.path import join as jn
import cv2

# CONSTANTS
path = os.getcwd()
itemRef = "agent_0"
SCALE = 128 #the scale is represented by the width in pixels of the horizontal axis

# Data def. RES
# res_% = int
# % is resolution
# interp. resolution of Arkanoid blocks
res_16 = 16
res_32 = 32
res_64 = 64


# Data def. LORES
# lores = [RES, RES, ...]
# interp. list of resolutions to tranform images
lores4 = [res_16 ,res_32 ,res_64]

# Data def. LOSPR
# lospr = [str, str, str]
# interp. list of sprites to resize
lospr0 = []
lospr1 = []

folder_substruct = []
for root, folders, files in os.walk(path):
    for folder in folders:
        lospr1 += [{"folder":folder, "file":jn(folder,file)} for file in os.listdir(jn(path,folder)) if file.endswith(".png")]


# Func. def. getMaxWidth()
# Signature: WIDTHS, <accumulator> -> <accumulator>
# purp. get index of the highest item number in the list
def getMaxWidth(WIDTHS, acc, poin):
    if acc == len(WIDTHS):
        return(poin)
    else:
        if WIDTHS[acc] > WIDTHS[poin]:
            score = getMaxWidth(WIDTHS, acc+1 ,acc)
        else:
            score = getMaxWidth(WIDTHS, acc+1 ,poin)
    return(score)


# Func. def. getMinWidth()
# Signature: WIDTHS, <accumulator> -> <accumulator>
# purp. get index of the lowest item number in the list

def getMinWidth(WIDTHS, acc, poin):
    if acc == len(WIDTHS):
        return(poin)
    else:
        if WIDTHS[acc] < WIDTHS[poin]:
            score = getMinWidth(WIDTHS, acc+1 ,acc)
        else:
            score = getMinWidth(WIDTHS, acc+1 ,poin)
    return(score)


# Func. def. scale()
# Signature: <cv2.image>, I_MAXWIDTH -> (int, int, int)
# purp. calculate the ratio at which the sprites will need to be multiplied to scale them at the same size
def scale(spr, res):
    sc = res/spr.shape[1]
    # new_w = int((im.shape[1] / WIDTHS[REFWIDTH])*res)
    # new_h = int((im.shape[1]/im.shape[0])*new_w)
    return(sc)
    


# Func. def. newDims()
# Signature: <cv2.image>, SCALE -> (int, int, int)
# purp. calculate the ratio at which the sprites will need to be multiplied to scale them at the same size
def newDims(im, SCALE):
    new_w = int(im.shape[1]*SCALE)
    new_h = int(im.shape[0]*SCALE)
    return((new_w, new_h))

# Func. def. changeRes()
# Signature: LOSPR, RES, PATHS -> None
# purp. change the resolution of the given sprites

def changeRes(lospr, res, PATH, new_dir):

    # Get the block's width, which will be the reference for the game's size
    # for spr in lospr:
    #     if itemRef in spr["file"]:
    #         print("Here")
    #         spr = cv2.imread(jn(PATH,spr["file"]), cv2.IMREAD_UNCHANGED)
    #         SCALE = scale(spr, res)
    #         break
    

    for spr in lospr:
        im_name = jn(PATH,spr["file"]) #where to find the image
        im = cv2.imread(im_name, cv2.IMREAD_UNCHANGED)
        height_ratio = im.shape[0]/im.shape[1] #ratio is height/width
        if im.shape[1] > res:
            new_dims = res, int(height_ratio * res)
        else:
            new_dims = (im.shape[1],im.shape[0])
            
        im = cv2.resize(im, new_dims)
        file_name = jn(new_dir,f"{spr['file']}")
        folder_name = jn(new_dir,spr["folder"])
        if not os.path.exists(folder_name):
            os.makedirs(folder_name, exist_ok=True)
        cv2.imwrite(file_name, im)


lores = [16,24,32,42,64, 128, 256]

for res in lores:
    new_dir = jn(path, f"res_{str(res)}")
    # if not os.path.exists(new_dir):
    #     os.makedirs(new_dir, exist_ok=True)

    changeRes(lospr1, res, path, new_dir)


