import os
import numpy as np
from .read_roi import read_roi_zip
from .io_utils import read_image, write_image
import cv2 as cv


def gen_mask_core(roi_dir: os.PathLike, original_segmentated_file: os.PathLike,
                  output_directory: os.PathLike, output_format:str, num_threads: int = 1):
    """
    This function generates a corrected segmentation mask based on a set of ROIs (Region of Interest)
    :param roi_dir (os.PathLike): path to the directory containing the ROI zip files
    :param original_segmentated_file (os.PathLike): path to the original segmented file to be corrected
    :param output_directory (os.PathLike): path to the directory where the corrected segmentation file should be saved
    :param output_format (str): format in which the output file should be saved (e.g., "KLB", "TIF", "H5", "NPY")
    :param num_threads (int, optional): number of threads to use when reading the original segmented file. Default is 1.
    :return: output_file (os.PathLike): path to the corrected segmentation file that was saved
    """
    base_dir = os.path.dirname(original_segmentated_file)
    file_name = os.path.basename(original_segmentated_file)
    file_prefix = os.path.splitext(file_name)[0]

    # Read the labeled mask
    Xi = read_image(original_segmentated_file, num_threads)
    slice_counts = Xi.shape[0]
    # Blank canvas to draw the contours into
    Xi[:, :, :] = 0
    # Load ROIs and color
    for i in range(0, slice_counts):
        roi_zip_file = os.path.join(roi_dir, file_prefix+"_"+str(i+1) + '.zip')
        # Check if label suffix exists
        if not os.path.exists(roi_zip_file):
            roi_zip_file = os.path.join(roi_dir, file_prefix+".label_"+str(i+1) + '.zip')
        if os.path.exists(roi_zip_file):
            roi_dict = read_roi_zip(roi_zip_file)
            for key in roi_dict.keys():
                try:
                    label_val = int(float(key.split("_")[1]))
                    coord_x = roi_dict[key]['x']
                    coord_y = roi_dict[key]['y']
                    coord_list = []
                    for j in range(0,len(coord_y)):
                        coord_list.append([coord_x[j],coord_y[j]])
                    contours = np.array(coord_list).reshape((-1,1,2)).astype(np.int32)
                    cv.drawContours(Xi[i,:,:], [contours], -1, color=(label_val, label_val, label_val), thickness=cv.FILLED)
                except ValueError:
                    print("Invalid ROI label: {0}".format(key))

    output_file = os.path.join(output_directory, file_prefix+"_SegmentationCorrected")
    output_file = write_image(Xi, output_file, output_format, num_threads)
    return output_file










