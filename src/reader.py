# -*- coding: utf-8 -*-

import os
import sys
import json
from PIL import Image

#path to the image that is to be red
path = ('./A.bmp')

#directory to witch unpack the image
directory = ('./work4')

#set the recursion limit, just to be safe
#also, the recursive filling of pixels is a far stretch
sys.setrecursionlimit(1000000)   #we must go deeper!

#recursive function, used to track whole area
#one area is defined by black borders (0) or (0,0,0)
#WARNING this script causes segmentation fault on larger images
#in virtualbox, due to low amount of memory allocated for the
#guest system and th python interpreter itself, also, it's
#very greedy; sudden, unexplained crashes are to be expected,
#it may use some improvements
def rec_rec_fill(
    newpix, #pixelmap of currently processed area
    pixels, #pixelmap of oryginal image processed so far
    i,      #row of current pixel processed
    j,      #column of current pixel processed
    size):  #size of the image
    
    #copy value from original image to new the one,
    #and clear it from the former
    newpix[i,j] = pixels[i,j]
    pixels[i,j] = 0
    
    #check on right
    if i + 1 < size[0] and pixels[i+1,j] != 0 and pixels[i+1,j] != (0,0,0):
        #if non-black, run itself
        rec_rec_fill(newpix, pixels, i+1, j, size)
    
    #check on left
    if i - 1 >= 0 and pixels[i-1,j] != 0 and pixels[i-1,j] != (0,0,0):
        #if non-black, run itself
        rec_rec_fill(newpix, pixels, i-1, j, size)
    
    #check on bottom
    if j + 1 < size[1] and pixels[i,j+1] != 0 and pixels[i,j+1] != (0,0,0):
        #if non-black, run itself        
        rec_rec_fill(newpix, pixels, i, j+1, size)
    
    #check on top
    if j - 1 >= 0 and pixels[i,j-1] != 0 and pixels[i,j-1] != (0,0,0):
        #if non-black, run itself        
        rec_rec_fill(newpix, pixels, i, j-1, size)
    
    return 0
    
#helper function, used to create new image (of an area),
#fill it accordingly and then save
def rec_fill(
    pixels,     #pixelmap of an oryginal image
    i,          #row (in pixels), where new area is detected
    j,          #column (in pixels), where new area is detected
    size,       #image size
    title,      #image label (name)
    directory): #directory, where image is to be saved
    
    #init new black image
    img = Image.new('RGB', (size[0],size[1]), "black")
    #load pixelmap of new image
    newpix = img.load()
    
    #run recursive function to recognize the whole area
    rec_rec_fill(newpix, pixels, i, j, size)
    
    #save image modified by recursive function
    img.save(directory + '/' + title + '.bmp')
    
    return 0

#ceck if the directory already exists
if not os.path.exists(directory):
    #if not, create it
    os.makedirs(directory)

#static list to create titles for areas
titles = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

#open image and load it's pixel map
img = Image.open(path)
pixels = img.load()

#init vars for future use, loop stop condition,
#list to hold area name, and data dictionary
looper = True
name = list((0,0))
D=dict()

#loop over unknown number of areas
while looper:
    #consider termination (previous might be the last)
    looper = False
    #loop over every pixel
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            #check every pixel if it's black
            #it basicaly stops on every nonblack pixel found,
            #then starts over, until a full pass reveals
            #no non-black pixels left in the image
            if pixels[i,j] != 0 and pixels[i,j] != (0,0,0):
                #and if it's not
                #create title label
                title = titles[name[0]]+titles[name[1]]
                #run recursive function to save it to file
                rec_fill(pixels, i, j, img.size, title, directory)
                #init neigh list (for automation)
                D[title] = list()
                #update name and check for overflow
                name[1] += 1
                if name[1] >= 26:
                    name[0] += 1
                    name[1] -= 26
                
                #an area has been found - break, the areas are continuous
                looper = True
                break
            
        if looper:
            #an area has been found - break, the areas are continuous
            break
        
#save json file with formatting, to ease neighbour-defining process
with open(directory + '/neigh.json', 'w') as neigh:
    neigh.write(json.dumps(D, sort_keys=True, indent=4))