# roi_convertor: Convert Segmentation Output to ROI and Back

## Installation 

### Install on Della

The tool is already installed on della.princeton.edu. Use the following commands to load the environment:  

```
module purge
module load anaconda3/2021.11
conda activate /projects/LIGHTSHEET/posfailab/ab50/tools/tf2-posfai
export LD_LIBRARY_PATH=/projects/LIGHTSHEET/posfailab/ab50/tools/keller-lab-block-filetype/build/src
```

#### Requesting compute node

Long-running commands like `generate-mask` and `generate-analytics` should not be run on the login node. Please use the 
command below to first request a compute-node and then setup the above environment there and run the command. 

The command to request for a compute-node is: 

```commandline
salloc --nodes=1 --ntasks=8 --mem=10G --time=02:00:00
```

### Install on your own machine

You can run the following commands to install the tool in your own conda environment.

#### Windows Install

1. Download and install **Python 3.9** version of Miniconda for Windows: https://docs.conda.io/en/latest/miniconda.html#windows-installers

2. **Login**, download and install Visual Studio 2022 Professional to build pyklb: https://visualstudio.microsoft.com/vs 

3. Open "Command Prompt" and create a conda environment and activate it:
```
conda create -n segmentation python=3.9
conda activate segmentation
```

4. Install the ROI convertor:
```
pip install git+https://github.com/abiswas-odu/roi_convertor.git
roi_convert --help
```

#### MacOS Install

1. Download and install **Python 3.9** version of Miniconda for MacOS: https://docs.conda.io/en/latest/miniconda.html#macos-installers

2. Open "Terminal" and create a conda environment and activate it:
```
conda create -n segmentation python=3.9
conda activate segmentation
```

3. Install the ROI convertor:
```
pip install git+https://github.com/abiswas-odu/roi_convertor.git
roi_convert --help
```

## Generating ROI Files from Segmentation Output for Correction 

**Commandline Options**
```roi_convert generate-roi --help```

**Example Command: Short Version** 

This produces the ROIs in a directory named ```stardist_rois``` in same directory as the input image
```
roi_convert generate-roi 
--orig_image_file /projects/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test/klbOut_Cam_Long_00257.lux.label.tif
```

The input can be in klb/h5/tif/npy formats with these extensions. 

**Example Command: Long Version** 

This produces the ROIs in a directory of your choice and in a format of your choice.
```
roi_convert generate-roi 
--orig_image_file /projects/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test/klbOut_Cam_Long_00257.lux.label.tif 
--output_dir test_rois
```

## Generating Segmented Image with Labels from ROIs

This command is used to generate segmented labeled image from ROIs and the file or **directory** pointing to the original image(s). 

**File Naming Conventions: The naming of the ROI zip files and the ROIs are very important for correct operation of the tool.** 

1. The ROI zip file for each slice must be named as <orig_image_file_name>_<slice_id>.zip.

2. Each ROI from ROI Manager must be named as <slice_id>_<label_id>. **Where the label_id connects the cell across slices.**   

**Commandline Options**

```roi_convert generate-mask --help```

**Example Command: Short Version** 

This assumes the ROIs are in a directory named ```stardist_rois``` in same directory as the original input image(s) used to generate the ROIs.
**The `--orig_image` parameter can be a single file or directory.** 

```
roi_convert generate-mask 
--orig_image /projects/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test
```

The original input image can be in klb/h5/tif/npy formats with these extensions.

**Example Command: Long Version**

This lets the user specify all the details. 

```
roi_convert generate-mask 
--orig_image /projects/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test 
--roi_dir stardist_rois 
--output_dir . 
--output_format klb
```

## Generating Hand Correction Guide for Segmented Image

This command is used to generate hand correction guide for segmented labeled images.

**Commandline Options**

```roi_convert generate-analytics --help```

**Example Command**

The command can take single images or whole directories with the segmented files named in the way ```stardist_inference``` names them. 

```
roi_convert generate-analytics 
--orig_image /tigress/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test_3/multi_test_klb 
--segmentation_image /tigress/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/test_3/multi_test_klb_segmentation 
--output_file hand_correction_guide.csv
```

The original input image can be in klb/h5/tif/npy formats with these extensions.

## Generating Diff Report 

This command is used to generate the list of differences between the original ROIs and the corrected ROIs.

**Commandline Options**

```roi_convert roi-diff --help```

**Example Command**

```
roi_convert roi-diff 
--orig_roi_dir orig_stardist_rois 
--corrected_roi_dir stardist_rois
```

# Generating and Visualizing Cropboxes on DELLA

To generate cropboxes and visualize the MIPs on DELLA, do the following: 

1. Copy the scripts into a folder of your choice:
```
cp /tigress/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/scripts/runGenCropboxes.cmd <MY PATH>
cp /tigress/LIGHTSHEET/posfailab/ab50/tools/roi_convertor/scripts/runVizCropboxes.cmd <MY PATH>
```
2. Edit the `runGenCropboxes.cmd` script with an editor after copying on your laptop or directly. Change the following lines:
```
IMAGE_PATH="/tigress/LIGHTSHEET/posfailab/ab50/data/210809_Cdx2_HaloYAP_H2B_mTmG_whole_embryo/stack_3_channel_2_obj_left_long"
OUT_DIR="/tigress/LIGHTSHEET/posfailab/ab50/data/210809_Cdx2_HaloYAP_H2B_mTmG_whole_embryo/stack_3_channel_2_obj_left_crop"
timestamp_min="0"
timestamp_max="10"
```
Point the IMAGE_PATH to your original KLB files and the OUT_DIR to any directory you want to save the cropbox results. 
Edit the `timestamp_min` and `timestamp_max` to the first and last frames. **Please test with a smaller range first!**

3. The code is talking about 2GB per frame. So, if you are running 100 images then set the memory required as 250GB in the line:
```
#SBATCH --mem=250G                # total memory per node 
```
It's near the top of the script. 

4. Run the script and wait for it to finish. 
```
sbatch runGenCropboxes.cmd 
```

5. Inspect the results log file. The run should produce a file called `slurm-42221536.out`. Read it: 
```commandline
cat slurm-42221536.out
```
If it says, **WARNING!!! Multiple crop boxes found. Need to select one for membrane cropping.**, then we have to view the profiles. 
Otherwise, the cropbox index is 0. Move to step 7. 

6. View the crop profiles. Download the crop_x.png files and view them. It is likely clear which is the correct cropbox. Note the cropbox index.

7. To generate the MIPs for the selected cropbox index, Edit the `runVizCropboxes.cmd` script with an editor after copying on your laptop or directly. Change the following lines:
```commandline
IMAGE_PATH="/tigress/LIGHTSHEET/posfailab/ab50/data/210809_Cdx2_HaloYAP_H2B_mTmG_whole_embryo/stack_3_channel_2_obj_left"
CROP_DIR="/tigress/LIGHTSHEET/posfailab/ab50/data/210809_Cdx2_HaloYAP_H2B_mTmG_whole_embryo/stack_3_channel_2_obj_left_crop"
timestamp_min="0"
timestamp_max="10"
crop_box_index="0"
```
Point the IMAGE_PATH to your original KLB files, and the CROP_DIR to the output directory from the previous script. 
Edit the `timestamp_min` and `timestamp_max` to the first and last frames. 
Finally, change the `crop_box_index` to the index of the cropbox you want to use. 

4. Run the script and wait for it to finish.
```
sbatch runVizCropboxes.cmd 
```

# Rescaling Images 


