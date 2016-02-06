# -*- coding: utf-8 -*-

import json
import Image
import math

#open dataset ready for work
jsonFile = open('mapa.json').read()

#function used to calculate distance between two areas,
#represented here as middle points of those areas (lists)
def dist(
    middleA,    #middle point of area A
    middleB):   #middle point of area B
        
    return math.sqrt((middleA[0]-middleB[0])**2 + (middleA[1]-middleB[1])**2)

#recursive function used to assign right colours to areas;
#the single most important part of the program
def iter_over(
    tempKeys,   #list representing the areas,
                #that still remain under consideration
                #to be coloured 
    data,       #full data structure representing processed image
    nextK,      #key representing currently processed area
    col):       #current colour used to paint areas
    
    #remove current area from list of considered areas
    tempKeys.remove(nextK)
    
    #check if the area is not already coloured
    if data[nextK]['col'] == 0 or data[nextK]['col'] == (0,0,0):
        #if it's not, assign a colour
        data[nextK]['col'] = colors[col-1] 
        #then remove all of it's neighbours from list of considered areas
        for v in data[nextK]['neigh']:
            if v in tempKeys:
                #but only if they are not yet removed
                #otherwise an error occurs
                tempKeys.remove(v)
    
    #check if the list of areas is empty after all this
    if not tempKeys:
        #if it is, stop recursion (stop condition)
        return 0
        
    else:
        #otherwise find first area off of list,
        #and calculate the distance between it and current area
        #they are used to initiate method used to find
        #the next closest area
        nextNextK = tempKeys[0]
        minD = dist(data[nextK]['middle'], data[nextNextK]['middle'])
        
        #now, check each area
        for k in sorted(tempKeys):
            #calculate distance to it
            d = dist(data[nextK]['middle'], data[k]['middle'])
            if d < minD:
                #and if it's closer than the last closer,
                #update minD (minimal distace) and change next area
                minD = d
                nextNextK = k
        
        #after all this, call itself with changed area list,
        #the same data and colour, and new area considerd in pass
        return iter_over(tempKeys, data, nextNextK, col)


#read data from json file
data = json.loads(jsonFile)

#get size of image kept in the data structure, then remove the field
#(for automation purposes), and initiate new canvas
size = data['size']
del data['size']
img = Image.new('RGB', (size[0],size[1]), "black") #new black image

#initiate list of areas (from data structure) 
#and colours to paint with (static)
keys = list()
for k,v in data.iteritems():
    keys.append(k)  
colors = [(255,0,0), (0,255,0), (0,0,255), (100,100,100)]

#iterate over every possible entry point
#in the best scenario, this executes only once
for k in sorted(keys):
    #iter over every colour to paint
    for col in range(1,5):
        #for each color, create new list of aras
        #considered to be painted with it
        tempKeys = list(keys)
        
        #start recursive function
        iter_over(tempKeys, data, k, col-1)
        
    #assume everything went well
    stop = 1
    #iter over all areas again
    for ik in sorted(keys):
        #check if an area is not colored
        if data[ik]['col'] == 0 or data[ik]['col'] == (0,0,0):
            #this means that the way areas were coloured is wrong
            #switch flag and exit this loop
            stop = 0
            break
    
    if stop == 1:
        #everything is painted well, exit the loop
        break
    
    else:
        #something went wrong
        if k == keys[-1]:
            #if this is the last key, exit with warning
            #either the algorythm is wrong,
            #or example is badly constructed
            print('Something went wrong! :(')
            print(k)
        
        else:
            #otherwise, clear colours from the image,
            #before staring anew
            for ik in sorted(keys):
                data[ik]['col'] = 0

#load pixel map of the clear, black image
pixels = img.load()

#iterate over every area and pixels it contains, then colour them
#(on the image) to correspondent colour
for k,v in data.iteritems():
    for x,y in v['pix']:
        pixels[x,y] = v['col']

#display the image
img.show();