import sys
import os
import time

start = time.process_time()

from glob import glob

try:
    from PIL import Image
except ImportError:
    import Image

gearTypes = ["helm"] # List of base types

# Strip the path and extension from the filename
def stripFilename(fname):
    print("Splitting: " + fname)
    return str(fname).split("\\")[-1].split(".")[0]

# Generate the image from the supplied paths
def generateImage(gearType, background, overlay1, overlay2, overlay3, overlay4, overlay5):
    filename = "output/" + gearType + "/" + stripFilename(background) + stripFilename(overlay1)
    background = Image.open(background)
    overlayImage = Image.open(overlay1)
    background.paste(overlayImage, (0, 0), overlayImage)

    if overlay3:
        filename += stripFilename(overlay3)
        overlayImage = Image.open(overlay3)
        background.paste(overlayImage, (0, 0), overlayImage)
    if overlay4:
        filename += stripFilename(overlay4)
        overlayImage = Image.open(overlay4)
        background.paste(overlayImage, (0, 0), overlayImage)

    # Uncomment if you want the combined image displayed in an image viewer immediately
    #background.show()

    background = background.convert("RGBA")

    print("Generated image: " + filename)
    background.save(filename + ".png", "PNG")

# Run for each gear type
for gearType in gearTypes:
    print("Generating all " + gearType)

    # Create output folder
    if not os.path.exists("output/" + gearType):
        os.mkdirs(os.path.join('output', gearType))

    # List all subfolders
    layerFolders = [f for f in glob(gearType + "/*/")]

    # Find all layers in each subfolder
    layers = []
    for layerFolder in layerFolders:
        currentLayers = [f for f in glob(layerFolder + "/*.png")]
        if currentLayers:
            # Add layers if the folder isn't empty
            layers.append(currentLayers)

    # Ensure we have 5 layers (even if they are empty)
    while len(layers) < 5:
        layers.append([None])

    # Generate every possible combination of layers for the gear
    for a in layers[0]:
        for b in layers[1]:
            for c in layers[2]:
                for d in layers[3]:
                    for e in layers[4]:
                    # Generate the image passing in each layer
                        generateImage(gearType, a, b, c, d, e)

print('Possibly successful layering!')