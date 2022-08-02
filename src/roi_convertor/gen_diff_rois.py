import sys
import zipfile

# Either file name or directory
orig_roi_dir = sys.argv[1]

curr_roi_dir = sys.argv[2]

for
zf = zipfile.ZipFile(zip_path)
for n in zf.namelist():