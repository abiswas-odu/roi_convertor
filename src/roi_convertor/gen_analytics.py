import numpy as np
import math
from skimage.measure import label, regionprops, regionprops_table
from skimage import morphology
from .io_utils import read_image
import os
from csbdeep.io import save_tiff_imagej_compatible


def append_hand_correction_guide(segmentation_image, orig_image, output_file, runFNTest=False):
    seg = read_image(segmentation_image)
    raw = read_image(orig_image)
    label_ids, exclude_ids, numcells, frame_false_negative = gen_hand_correction_guide(seg, raw)
    file_name = os.path.basename(segmentation_image)
    file_prefix = os.path.splitext(file_name)[0]
    op_summary_file = os.path.join(output_file)
    printHeader = True
    if os.path.exists(op_summary_file):
        printHeader = False
    with open(op_summary_file, 'a') as out_f:
        if printHeader:
            out_f.write("frame_name, cell_count, cell_labels, false_pos_labels, false_neg_flag\n")
        out_f.write(file_prefix + ',')
        out_f.write(str(numcells) + ',')
        for label in label_ids:
            out_f.write(str(label) + '|')
        out_f.write(',')
        for label in exclude_ids:
            out_f.write(str(label) + '|')
        out_f.write(',')
        out_f.write(str(frame_false_negative) + '\n')


def gen_hand_correction_guide(seg, raw, run_fn_test=False):
    background_std_threshold = 2
    volume_threshold = 3000
    cell_std_threshold = 2
    # Exclude regions in segmented image whose mean intensities are within 2 stds of the background

    foreground_ind = np.nonzero(seg)
    num_bg = seg.size - len(foreground_ind[0])
    s_all = sum(raw.sum(axis=(1, 2)))
    s_foreground = np.sum(raw[foreground_ind])
    background_mean = (s_all - s_foreground) / num_bg

    # Sum of squares
    ss_all = np.sum(np.square(raw - background_mean))
    ss_foreground = np.sum(np.square(raw[foreground_ind] - background_mean))
    ss_bg = ss_all - ss_foreground
    background_std = math.sqrt(ss_bg / (num_bg - 1))

    # label_img, label_counts = label(seg, return_num=True)
    # save_tiff_imagej_compatible("test.tif", seg.astype('uint16'), axes='ZYX')
    stats = regionprops(seg, raw)
    exclude_id = []
    label_ids = []
    cell_intensities = []
    numcells = 0
    for region in stats:
        label_ids.append(region.label)
        if not math.isnan(region.mean_intensity):
            if (region.mean_intensity - background_mean) < (background_std_threshold * background_std):
                exclude_id.append(region.label)
            else:
                numcells = numcells + 1
                cell_intensities.append(region.mean_intensity)

    cell_intensity_mean = np.mean(np.array(cell_intensities))
    cell_intensity_std = np.std(np.array(cell_intensities))

    # False negative alert!
    frame_false_negative = False
    if run_fn_test:
        raw_subtract = raw
        seg[np.nonzero(seg)] = 1
        img_dilation = morphology.binary_dilation(seg, morphology.ball(radius=10))
        raw_subtract[np.nonzero(img_dilation)] = background_mean
        BW = np.where(raw_subtract > (background_mean + 2 * background_std), 1, 0)
        BW = morphology.remove_small_objects(BW, min_size=100, connectivity=26)

        stats_BW = regionprops(BW, raw_subtract)
        for region in stats_BW:
            if (region.area > volume_threshold) and \
                    (region.mean_intensity - cell_intensity_mean) < (cell_std_threshold * cell_intensity_std):
                frame_false_negative = True
                break
    return label_ids, exclude_id, numcells, frame_false_negative
