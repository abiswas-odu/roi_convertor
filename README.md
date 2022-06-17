# roi_convertor: Convert Segmentation Output to ROI and Back

## Installation 

### Install on Della

The tool is already installed on della.princeton.edu. Use the following commands to load the environment:  

```
module load anaconda3/2021.11
conda activate /projects/LIGHTSHEET/posfailab/ab50/tools/tf2-posfai
export LD_LIBRARY_PATH=/projects/LIGHTSHEET/posfailab/ab50/tools/keller-lab-block-filetype/build/src
```

### Install on your own machine

You can run the following commands to install the tool in your own conda environment. I have intentionally separated the 
pyklb install because it causes problems on certain machines. So you must ensure that you have it installed correctly on 
your machine. 
```
# Try the wheels build; Did not work for me. I had to compile the binary.  
pip install git+https://github.com/bhoeckendorf/pyklb.git@skbuild

# Once pyklb is installed... 
git clone https://github.com/abiswas-odu/roi_convertor.git
cd roi_convertor
pip install .
```

## Generating ROI Files from Segmentation Output for Correction 

### Commandline Options

```roi_convert generate-roi --help```

### Example Command: Short Version 

This produces the ROIs in a directory named ```stardist_rois``` in same directory as the input image

```roi_convert generate-roi --orig_image_file /projects/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test/klbOut_Cam_Long_00257.lux.label.tif```

The input can be in klb/h5/tif/npy formats with these extensions. 

### Example Command: Long Version 

This produces the ROIs in a directory of your choice and in a format of your choice

```roi_convert generate-roi --orig_image_file /projects/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test/klbOut_Cam_Long_00257.lux.label.tif --output_dir test_rois```

## Generating Segmented Image with Labels from ROIs

This command is used to generate segmented labeled image from ROIs. 

### File Naming Conventions 

**The naming of the ROI zip files and the ROIs are very important for correct operation of the tool.** 

1. The ROI zip file for each slice must be named as <orig_image_file_name>_<slice_id>.zip.

2. Each ROI from ROI Manager must be named as <slice_id>_<label_id>. **Where the label_id connects the cell across slices.**   

### Commandline Options

```roi_convert generate-mask --help```

### Example Command: Short Version 

This assumes the ROIs are in a directory named ```stardist_rois``` in same directory as the original input image used to generate the ROIs

```roi_convert generate-mask --orig_image_file /projects/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test/klbOut_Cam_Long_00257.lux.label.tif```

The original input image can be in klb/h5/tif/npy formats with these extensions.

### Example Command: Long Version

This lets the user specify all the details. 

```roi_convert generate-mask --orig_image_file /projects/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test/klbOut_Cam_Long_00257.lux.label.tif --roi_dir stardist_rois --output_dir . --output_format klb ```
