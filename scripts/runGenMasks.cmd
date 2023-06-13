#!/bin/bash

#SBATCH --job-name=gen_crops     # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=10              # total number of tasks across all nodes
#SBATCH --mem=10G                # total memory per node
#SBATCH --time=1:00:00           # total run time limit (HH:MM:SS)
#SBATCH -A molbio


IMAGE_PATH="/projects/LIGHTSHEET/posfailab/mchalifoux/Raw_data/210809_stack3/membrane"
OUT_DIR="/tigress/LIGHTSHEET/posfailab/ab50/tools/stardist_inference/test/data/membrane_rescale"
timestamp_min="0"
timestamp_max="10"
crop_box_index="1"


##===================================================================================================
##=====================CHANGES BELOW THIS LINE FOR ADVANCED USERS====================================
##===================================================================================================

filter_window_size="100"
threshold_after_filter="0.1"
generate_plots="True"
num_threads="10"

##===================================================================================================
##==============================NO CHANGES BELOW THIS LINE===========================================
##===================================================================================================

echo Running on host `hostname`
echo Starting Time is `date`
echo Directory is `pwd`
starttime=$(date +"%s")

module purge
module load anaconda3/2020.11
export LD_LIBRARY_PATH=/projects/LIGHTSHEET/posfailab/ab50/tools/keller-lab-block-filetype/build/src
conda activate /projects/LIGHTSHEET/posfailab/ab50/tools/tf2-posfai

roi_convert crop-images --orig_image_dir ${IMAGE_PATH} \
  --crop_file_dir ${OUT_DIR} \
  --cropbox_index ${crop_box_index} \
  --output_dir ${OUT_DIR} \
  -tb ${timestamp_min} \
  -te ${timestamp_max} \
  --num_threads ${num_threads}

echo Ending time is $(date)
endtime=$(date +"%s")
diff=$(($endtime - $starttime))
echo Elapsed time is $(($diff/60)) minutes and $(($diff%60)) seconds.

