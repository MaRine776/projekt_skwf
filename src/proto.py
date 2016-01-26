# -*- coding: utf-8 -*-

import json
import Image

jsonFile = open('mapa.json').read()

data = json.loads(jsonFile)

img = Image.new('RGB', (data['size'][0],data['size'][1]), "black") #new black image
del data['size']

keys = []
for k,v in data.iteritems():
    keys.append(k)  #there is unknown number of areas
    
colors = [(255,0,0), (0,255,0), (0,0,255), (100,100,100)] #colors to paint with
    
for i in range(1,5):    #there is always four colors
    tempKeys = list(keys)
    
    for k in sorted(keys):
        if k in sorted(tempKeys):
            if data[k]['col'] != 0:
                tempKeys.remove(k)
                
            else:
                tempKeys.remove(k)
                data[k]['col'] = colors[i-1]
                
                for v in data[k]['neigh']:
                    if v in tempKeys:
                        tempKeys.remove(v)
    
    
pixels = img.load() #pixel map

for k,v in data.iteritems():
    for x,y in v['pix']:
        pixels[y-1,x-1] = v['col']

img.show();