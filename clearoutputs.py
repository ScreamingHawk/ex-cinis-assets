import shutil
from glob import glob

# Deletes all folders inside the "output" and "token_data" folders
[shutil.rmtree(f) for f in glob("output/*/")]
[shutil.rmtree(f) for f in glob("token_data/")]
