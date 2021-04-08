import sys
import os
import time
from glob import glob

try:
    from PIL import Image
except ImportError:
    import Image

gearTypes = ["helm"] # List of base types

# Strip the path and extension from the filename
def stripFilename(fname):
    return str(fname).split("\\")[-1].split(".")[0]

# Generate the image from the supplied paths
def generateImage(gearType, background, layers):
    filename = "output/" + gearType + "/" + stripFilename(background)
    background = Image.open(background)

    background = background.convert("RGBA")

    for layer in layers:
        if layer is not None:
            filename += stripFilename(layer)
            overlayImage = Image.open(layer)
            background.paste(overlayImage, (0, 0), overlayImage)

    # Uncomment if you want the combined image displayed in an image viewer immediately
    #background.show()

    print("Generated image: " + filename)
    background.save(filename + ".png", "PNG")

startTotal = time.time()

# Read common backgrounds
backgrounds = [f for f in glob("backgrounds/*.png")]

# Run for each gear type
for gearType in gearTypes:
    start = time.time()
    print("Generating all " + gearType)

    # Create output folder
    if not os.path.exists("output/" + gearType):
        os.makedirs(os.path.join('output', gearType))

    # List all subfolders
    layerFolders = [f for f in glob(gearType + "/*/")]

    # Find all layers in each subfolder
    layers = []
    for layerFolder in layerFolders:
        currentLayers = [f for f in glob(layerFolder + "/*.png")]
        if currentLayers:
            # Add layers if the folder isn't empty
            layers.append(currentLayers)

    # Ensure we have 4 layers (even if they are empty)
    while len(layers) < 4:
        layers.append([None])

    # Generate every possible combination of layers for the gear
    for background in backgrounds:
        for a in layers[0]:
            for b in layers[1]:
                for c in layers[2]:
                    for d in layers[3]:
                        # Generate the image passing in each layer
                        generateImage(gearType, background, [a, b, c, d])

    # Print how long it took to do a whole gear type
    print("Generating {} took {:.2f} seconds".format(gearType, time.time()-start))

print("All together it took {:.2f} seconds".format(time.time()-startTotal))
print('Possibly successful layering!')