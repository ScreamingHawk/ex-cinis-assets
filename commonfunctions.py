# A file for common shared functions

from glob import glob
from time import strptime

def listGearTypes():
    """ Return a list of base gear types. """
    return ["helm" ,"chest"]

def stripFilename(fname):
    """ Strip the path and extension from the filename. """
    return str(fname).split("\\")[-1].split(".")[0]

def listAllBackgrounds():
    """ Read common backgrounds. """
    return [f for f in glob("backgrounds/*.png")]

def listAllPalettes():
    """ List all available palettes """
    return [f for f in glob("palette/*.png")]

def listAllLayers(gearType):
    """ List all layers for given gear type. """
    # List all subfolders
    layerFolders = [f for f in glob(gearType + "/*/")]

    # Find all layers in each subfolder
    layers = []
    for layerFolder in layerFolders:
        currentLayers = [f for f in glob(layerFolder + "/*.png")]
        if currentLayers:
            # Add layers if the folder isn't empty
            layers.append(currentLayers)

    return layers

def generateImageFilename(gearType, background, layers, palette):
    """ Generate image filename from the supplied paths. """
    filename = f"output/{gearType}/{stripFilename(palette)}/{stripFilename(background)}/"

    for layer in layers:
        if layer is not None:
            filename += stripFilename(layer)

    return filename + ".png"