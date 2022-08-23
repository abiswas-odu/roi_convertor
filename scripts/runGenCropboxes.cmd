#!/bin/bash

#SBATCH --job-name=sd_infer      # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --mem=100G               # total memory per node
#SBATCH --time=1:00:00           # total run time limit (HH:MM:SS)
#SBATCH -A molbio


IMAGE_PATH="/tigress/LIGHTSHEET/posfailab/ab50/data/210809_Cdx2_HaloYAP_H2B_mTmG_whole_embryo/stack_3_channel_2_obj_left"
OUT_DIR="/tigress/LIGHTSHEET/posfailab/ab50/data/210809_Cdx2_HaloYAP_H2B_mTmG_whole_embryo/stack_3_channel_2_obj_left_crop"
OUT_FORMAT="klb"

##===================================================================================================
##=====================CHANGES BELOW THIS LINE FOR ADVANCED USERS====================================
##===================================================================================================

timestamp_min="50"
timestamp_max="55"

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

roi_convert generate-cropboxes --orig_image_dir ${IMAGE_PATH} \
  --output_dir ${OUT_DIR} \
  -tb 50 \
  -te 55 \
  --generate_plots \
  --gen_mip_viz \
  -ws 100 \
  -thresh 0.1

echo Ending time is $(date)
endtime=$(date +"%s")
diff=$(($endtime - $starttime))
echo Elapsed time is $(($diff/60)) minutes and $(($diff%60)) seconds.

