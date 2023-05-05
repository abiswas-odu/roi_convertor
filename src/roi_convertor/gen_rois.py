import tifffile as tif
import os
import numpy as np
import cv2 as cv
from .roi_encoder import encode_ij_freehand_roi
from .io_utils import read_image
import zipfile


def extract_borders(label_image):
    """Obtain a dictionary with the points forming the contours of each region with the same vale in the 2-d array
    Args:
        Xi: 2-dimensional numpy array with the image pixels.
    Returns:
        Dictionary {label_value, [list of points(x,y)]}
    """
    labels = np.unique(label_image[label_image > 0])
    d = {}
    for label in labels:
        y = label_image == label
        y = y * 255
        y = y.astype('uint8')
        contours, hierarchy = cv.findContours(y, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if len(contours) > 1:
            for i in range(0, len(contours)):
                d[label + i/10] = np.squeeze(contours[i]).tolist()
        else:
            contours = np.squeeze(contours)
            d[label] = contours.tolist()
    return d


def roi_generator_core(Xi, file_prefix, output_dir):
    """Generate the ROI files for each frame of the N-dimensional numpy array.
    Args:
        Xi: N-dimensional numpy array.
        file_prefix: Prefix string for the ROI file names.
        output_dir: The directory to produce the files.
    Returns:
        Dictionary with the label count summary for each frame
    """
    slice_counts = Xi.shape[0]
    label_summary_dict={}
    for i in range(0, slice_counts):
        label_contours_dict = extract_borders(Xi[i,:,:])
        if len(label_contours_dict) > 0:
            label_list = []
            with zipfile.ZipFile(os.path.join(output_dir,file_prefix+"_"+str(i+1) + '.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
                for key in label_contours_dict.keys():
                    label_list.append(key)
                    freehand_points = np.array(label_contours_dict[key]).T
                    if freehand_points.ndim > 1:
                        roi_file_name = str(i+1) + "_" + str(key) + ".roi"
                        f = open(roi_file_name,"wb")
                        if freehand_points[0].shape == freehand_points[1].shape:
                            f.write(encode_ij_freehand_roi(str(key), i+1, freehand_points[0].tolist(), freehand_points[1].tolist()))
                        else:
                            print("Error! size mismatch in coordinate lists. Slice " + str(i+1) + " Label " + str(key))
                        f.close()
                        zipf.write(roi_file_name)
                        os.remove(roi_file_name)
            label_summary_dict[i] = label_list
    return label_summary_dict


def gen_roi(input_file: os.PathLike, output_dir: os.PathLike = "", num_threads: int = 1):
    """Generate the ROI files for each frame of the image in in klb/h5/tif/npy format. It creates a folder stardist_rois
    in the same folder as the input image.
    Args:
        image_file: Path to the image file in klb/h5/tif/npy format with the same extensions respectively.
        output_dir: Output dir.
        num_threads: Number of threads.
    Returns:
        Directory where the ROI files are saved
    """
    base_dir = os.path.dirname(input_file)
    file_name = os.path.basename(input_file)
    file_prefix = os.path.splitext(file_name)[0]
    if not output_dir:
        output_dir = os.path.join(base_dir,"stardist_rois")
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    Xi = read_image(input_file, num_threads)
    label_summary_dict = roi_generator_core(Xi,file_prefix,output_dir)

    with open(os.path.join(base_dir,file_prefix + '_summary.csv'), 'w') as out_f:
        out_f.write("slice_id, object_count, object_labels\n")
        for key in label_summary_dict.keys():
            out_f.write(str(key+1) + "," + str(len(label_summary_dict[key])) + ",")
            for label in label_summary_dict[key]:
                out_f.write(str(label) + "|")
            out_f.write("\n")
    return output_dir

def gen_roi_narray(Xi, segmentation_file_name):
    """Generate the ROI files for each frame of the image in in klb/h5/tif/npy format. It creates a folder stardist_rois
    in the same folder as the input image.
    Args:
        Xi: N-dimensional numpy array.
        segmentation_file_name: name and path of the segmentation output file for the ROI file names.
    Returns:
        Directory where the ROI files are saved
    """
    base_dir = os.path.dirname(segmentation_file_name)
    file_name = os.path.basename(segmentation_file_name)
    file_prefix = os.path.splitext(file_name)[0]
    output_dir = os.path.join(base_dir,"stardist_rois")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    Xi = Xi.astype(dtype=np.uint8)
    label_summary_dict = roi_generator_core(Xi,file_prefix, output_dir)

    op_summary_file = os.path.join(base_dir,file_prefix + '_summary.csv')
    with open(op_summary_file, 'w') as out_f:
        out_f.write("slice_id, object_count, object_labels\n")
        for key in label_summary_dict.keys():
            out_f.write(str(key+1) + "," + str(len(label_summary_dict[key])) + ",")
            for label in label_summary_dict[key]:
                out_f.write(str(label) + "|")
            out_f.write("\n")
    return op_summary_file


#contours,hierarchy = cv.findContours(Xi[23,:,:], cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
#
# cv.imwrite("filename.png", Xi[23,:,:])
# img = cv.imread("filename.png")
# cv.drawContours(img, contours, 8, (0, 255, 0), 1, hierarchy=hierarchy, maxLevel=2)
# cv.imshow('Contours', img)
# cv.waitKey(0)
# cv.destroyAllWindows()


