import shutil
from glob import glob

# Deletes all folders inside the "output" folder
[shutil.rmtree(f) for f in glob("output/*/")]
