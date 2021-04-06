import sys
import os

os.chdir(sys.path[0])

#os.listdir(path)
#set the working directory to script location
try:
    from PIL import Image
except ImportError:
    import Image
background = Image.open(r"helm\headbase\headbase1.png")
overlay1 = Image.open(r"helm\mouthpiece\mouthpiece1.png")
overlay2 = Image.open(r"helm\earpiece\earpiece1.png")
overlay3 = Image.open(r"helm\visor\visor1.png")

background.paste(overlay1, (0, 0), overlay1)
background.paste(overlay2, (0, 0), overlay2)
background.paste(overlay3, (0, 0), overlay3)
#background.show()
#uncomment above if you want the combined image displayed in an image viewer immediately

background = background.convert("RGBA")
#I really don't know what this does but it might be important

background.save("combined.png","PNG")
#save the image in the script location

print ('Possibly successful layering!')