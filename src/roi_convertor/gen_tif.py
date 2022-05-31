import tifffile as tif
import os
import numpy as np
from .read_roi import read_roi_zip
from .io_utils import read_image, write_image
import cv2 as cv

def gen_mask_core(roi_dir, original_segmentated_file, output_directory, output_format):
    base_dir = os.path.dirname(original_segmentated_file)
    file_name = os.path.basename(original_segmentated_file)
    file_prefix = os.path.splitext(file_name)[0]

    # Read the labeled mask
    Xi = read_image(original_segmentated_file)
    slice_counts = Xi.shape[0]

    # Load ROIs and color
    for i in range(0, slice_counts):
        roi_zip_file = os.path.join(roi_dir, file_prefix+"_"+str(i+1) + '.zip')
        if os.path.exists(roi_zip_file):
            roi_dict = read_roi_zip(roi_zip_file)
            Xi[i,:,:] = 0
            for key in roi_dict.keys():
                label_val = int(float(key.split("_")[1]))
                coord_x = roi_dict[key]['x']
                coord_y = roi_dict[key]['y']
                coord_list = []
                for j in range(0,len(coord_y)):
                    coord_list.append([coord_x[j],coord_y[j]])
                #contours = np.array(coord_list)
                contours = np.array(coord_list).reshape((-1,1,2)).astype(np.int32)
                cv.drawContours(Xi[i,:,:], [contours], -1, color=(label_val, label_val, label_val), thickness=cv.FILLED)

    output_file = os.path.join(output_directory, file_prefix+"_HandCorrected.tif")
    write_image(Xi, output_file, output_format)
    return output_file

def gen_tif(input_file):
    base_dir = os.path.dirname(input_file)
    file_name = os.path.basename(input_file)
    file_prefix = os.path.splitext(file_name)[0]
    roi_dir = os.path.join(base_dir, "stardist_rois")
    output_file = gen_mask_core(roi_dir, input_file, roi_dir, "tif")
    return output_file









