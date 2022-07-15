import numpy as np
import math
from skimage.measure import label, regionprops, regionprops_table
from skimage import morphology
from csbdeep.io import save_tiff_imagej_compatible

def gen_hand_correction_guide(seg, raw):
    background_std_threshold = 2
    volume_threshold = 3000
    cell_std_threshold = 2
    # Exclude regions in segmented image whose mean intensities are within 2 stds of the background

    foreground_ind = np.nonzero(seg)
    num_bg = seg.size - len(foreground_ind[0])
    s_all = sum(raw.sum(axis=(1, 2)))
    s_foreground = np.sum(raw[foreground_ind])
    background_mean = (s_all - s_foreground) / num_bg

    #Sum of squares
    ss_all = np.sum(np.square(raw-background_mean))
    ss_foreground = np.sum(np.square(raw[foreground_ind]-background_mean))
    ss_bg = ss_all - ss_foreground
    background_std = math.sqrt(ss_bg / (num_bg - 1))

    # label_img, label_counts = label(seg, return_num=True)
    # save_tiff_imagej_compatible("test.tif", seg.astype('uint16'), axes='ZYX')
    stats = regionprops(seg, raw)
    exclude_id = []
    cell_intensities = []
    numcells = 0
    for region in stats:
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
    return exclude_id, numcells, frame_false_negative



