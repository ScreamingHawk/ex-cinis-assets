import os
import time
from multiprocessing import Pool
import itertools
from commonfunctions import *
import numpy as np

try:
    from PIL import Image
except ImportError:
    import Image

# Generate the image from the supplied paths
def generateImage(gearType, background, layers, palette):
    base_img = Image.open(background)
    img_arr = np.array(base_img) # Image to numpy array (a 2D array, since it was a P type image; does not include palette data)

    for layer in layers:
        if layer is not None:
            overlay = Image.open(layer)
            overlay_arr = np.array(overlay) # Image to np array

            # Place element from overlay array onto the output image array where it's not 0 (or not transparent, as 0 -> transparent according to palette)
            img_arr = np.where(overlay_arr == 0, img_arr, overlay_arr)

    # <redacted>
    #background.show()

    # Load the current palette to apply
    plt = Image.open(palette).getpalette()

    #convert output image array to image, and assign the correct palette
    out_img = Image.fromarray(img_arr, mode = 'P')
    out_img.putpalette(plt) # Assigning the palette as per the base image

    filename = generateImageFilename(gearType, background, layers, palette)
    #print("Generated image: " + filename)
    out_img.save(filename, "PNG")

def generateGearTypeImagesForRarity(gearType, background, palette):
    #start = time.time()

    print(f"Generating all {gearType} for {background} with {palette}")

    # Create output folder
    out_path = f"output/{gearType}/{stripFilename(palette)}/{stripFilename(background)}"
    if not os.path.exists(out_path):
        try:
            os.makedirs(out_path)
        except FileExistsError:
            # Race condition due to threading
            pass

    layers = listAllLayers(gearType)

    # Ensure we have 4 layers (even if they are empty)
    while len(layers) < 4:
        layers.append([None])

    # Generate every possible combination of layers for the gear
    for a in layers[0]:
        for b in layers[1]:
            for c in layers[2]:
                for d in layers[3]:
                    # Generate the image passing in each layer
                    generateImage(gearType, background, [a, b, c, d], palette)

    # Print how long it took to do a whole gear type
    #print("Generating {} took {:.2f} seconds".format(gearType, time.time()-start))

if __name__ == "__main__":
    startTotal = time.time()

    # backgrounds = ['backgrounds\\nbg_1.png'] # For testing 
    # palettes = ['palette\\ExCinis_BrassDragon.png'] # For testing 

    #Use 4 cores
    with Pool(processes=4) as pool:
        pool.starmap(generateGearTypeImagesForRarity, itertools.product(listGearTypes(), listAllBackgrounds(), listAllPalettes()))

    print("All together it took {:.2f} seconds".format(time.time()-startTotal))
    print('Possibly successful layering!')