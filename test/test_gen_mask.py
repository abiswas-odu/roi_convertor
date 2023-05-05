from src.roi_convertor.io_utils import read_image, write_image
from src.roi_convertor.gen_tif import gen_mask_core
import os
import numpy as np


def test_gen_tif():
    base_dir = 'data/generate_roi'
    roi_dir = os.path.join(base_dir, "compare_stardist_rois")
    original_segmentated_file = os.path.join(base_dir, 'klbOut_Cam_Long_00258.lux.label.tif')
    X_orig = read_image(original_segmentated_file)
    generated_mask_file = gen_mask_core(roi_dir, original_segmentated_file, base_dir, "tif")
    X_gen = read_image(generated_mask_file)
    assert os.path.isfile(generated_mask_file) == True
    diff_count = np.sum(X_orig != X_gen)
    assert diff_count == 6


def test_gen_klb():
    base_dir = 'data/generate_roi'
    roi_dir = os.path.join(base_dir, "compare_stardist_rois")
    original_segmentated_file = os.path.join(base_dir, 'klbOut_Cam_Long_00258.lux.label.klb')
    X_orig = read_image(original_segmentated_file)
    generated_mask_file = gen_mask_core(roi_dir, original_segmentated_file, base_dir, "klb")
    X_gen = read_image(generated_mask_file)
    assert os.path.isfile(generated_mask_file) == True
    diff_count = np.sum(X_orig != X_gen)
    assert diff_count == 6