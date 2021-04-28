import sys
import os
import time
from glob import glob
from multiprocessing import Pool
import itertools

import commonfunctions

try:
    from PIL import Image
except ImportError:
    import Image

# Generate the image from the supplied paths
def generateImage(gearType, background, layers):
    img = Image.open(background)

    img = img.convert("RGBA")

    for layer in layers:
        if layer is not None:
            overlayImage = Image.open(layer)
            try:
                img.paste(overlayImage, (0, 0), overlayImage)
            except ValueError as e:
                print("Error generating image for files: " + background + ", " + ", ".join(layers))
                print("Error image specifically: " + layer)
                raise e

    # Uncomment if you want the combined image displayed in an image viewer immediately
    #background.show()

    filename = commonfunctions.generateImageFilename(gearType, background, layers)
    #print("Generated image: " + filename)
    img.save(filename, "PNG")

def generateGearTypeImagesForRarity(gearType, background):
    start = time.time()
    print("Generating all " + gearType + " for " + background)

    # Create output folder
    if not os.path.exists("output/" + gearType):
        try:
            os.makedirs(os.path.join('output', gearType))
        except FileExistsError:
            # Race condition due to threading
            pass

    layers = commonfunctions.listAllLayers(gearType)

    # Ensure we have 4 layers (even if they are empty)
    while len(layers) < 4:
        layers.append([None])

    # Generate every possible combination of layers for the gear
    for a in layers[0]:
        for b in layers[1]:
            for c in layers[2]:
                for d in layers[3]:
                    # Generate the image passing in each layer
                    generateImage(gearType, background, [a, b, c, d])

    # Print how long it took to do a whole gear type
    print("Generating {} took {:.2f} seconds".format(gearType, time.time()-start))

if __name__ == "__main__":
    startTotal = time.time()

    backgrounds = commonfunctions.listAllBackgrounds()

    # Use 4 cores
    with Pool(processes=4) as pool:
        pool.starmap(generateGearTypeImagesForRarity, itertools.product(commonfunctions.listGearTypes(), backgrounds))

    print("All together it took {:.2f} seconds".format(time.time()-startTotal))
    print('Possibly successful layering!')
