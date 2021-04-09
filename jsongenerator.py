import sys
import os
import time
from glob import glob
from multiprocessing import Pool
import itertools
import json

import commonfunctions

basePath = 'https://raw.githack.com/superepicgecko/ex-cinis-assets/master/'

# Generate the image from the supplied paths
def generateJSON(gearType, background, layers, gearData):
    data = {}
    data['image'] = basePath + commonfunctions.generateImageFilename(gearType, background, layers)
    data['description'] = 'Ex Cinis {}'.format(gearType)
    data['name'] = gearData #FIXME Replace this with something using the layer names

    with open('token_data/{}.json'.format(gearData), 'w') as fout:
        fout.write(json.dumps(data))

def leadingZeros(num):
    """ Converts a number to a string of 2 digits with leading zeros. """
    return "{:02d}".format(num)

def generateAllJSON():

    backgrounds = commonfunctions.listAllBackgrounds()
    gearTypes = commonfunctions.listGearTypes()

    for ig, gearType in enumerate(gearTypes):
        layers = commonfunctions.listAllLayers(gearType)
        # Ensure we have 4 layers (even if they are empty)
        while len(layers) < 4:
            layers.append([None])

        for ib, background in enumerate(backgrounds):
            for i0, a in enumerate(layers[0]):
                for i1, b in enumerate(layers[1]):
                    for i2, c in enumerate(layers[2]):
                        for i3, d in enumerate(layers[3]):
                            gearData = str(ib + 1) + str(ig + 1) + leadingZeros(i0) + leadingZeros(i1) + leadingZeros(i2) + leadingZeros(i3)
                            generateJSON(gearType, background, [a, b, c, d], gearData)

if __name__ == "__main__":
    startTotal = time.time()

    # Create output folder
    if not os.path.exists("token_data/"):
        os.makedirs(os.path.join('token_data'))

    # Run the generator
    generateAllJSON()

    print("All together it took {:.2f} seconds".format(time.time()-startTotal))
    print('Possibly successful layering!')