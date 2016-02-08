
# -*- coding: utf-8 -*-
import json
from PIL import Image
import os

#open directory to parse into json file
directory = ('./work5')

#list work directory
work = os.listdir(directory)

#remove 'neigh.json' file from dir list (for automation)
work.remove('neigh.json')

#open json file with neighbours and load it's contents
jsonFile = open(directory + '/neigh.json').read()
neigh = json.loads(jsonFile)

#fill sparse neighbours matrix
for k, v in neigh.iteritems():
    for i in v:
        if neigh[i].count(k) == 0:
            #but only for unknown neighrours
            neigh[i].append(k)
        
#initialize python dictionary
D=dict()

#iterate over every file in directory
for k in work:
    #open current file
    print(k)
    img = Image.open(directory + '/' + k)
    #initialize number of pixls (to calculate middle)
    num = 0
    #we preassume the area is represented by a key,
    #and that the filename equals to [key].***, thus
    #we remove last 4 characters of filename to get the key
    sgn = k[:-4]
    #initialize area dictionary, inside main data dictionary
    D[sgn] = dict()
    #add it's neighbours
    D[sgn]['neigh'] = neigh[sgn]
    #set it's colour (0 = none)
    D[sgn]['col'] = 0
    #initialize list of it's pixels
    D[sgn]['pix'] = list()
    #initialize list of middle dimensions (2 for image)
    D[sgn]['middle'] = list()
    D[sgn]['middle'].append(0)
    D[sgn]['middle'].append(0)
    #set image size; this is overridden with each pass,
    #but alternatives are slower and less convinient
    D['size'] = img.size
    #load pixel list from image
    pixels = img.load()
    #iterate over all pixels in image
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i,j] != (0,0,0) and pixels[i,j] != 0:
                #if considered pixel is not black
                #assign it to current area
                #and proceed with middle calculations
                num += 1
                D[sgn]['middle'][0] += i
                D[sgn]['middle'][1] += j
                D[sgn]['pix'].append((i,j))
    
    #divide sum, to get middle coords
    D[sgn]['middle'][0] /= num
    D[sgn]['middle'][1] /= num
    
#write all data to a json file
with open('mapa.json', 'w') as out:
    out.write(json.dumps(D, sort_keys=True, indent=4))
