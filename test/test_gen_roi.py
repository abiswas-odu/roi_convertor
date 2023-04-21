from src.roi_convertor.gen_rois import gen_roi
from .test_utils import *
import os.path
import shutil


def test_gen_roi_tif():
    base_dir = 'data/generate_roi'
    segmented_file = os.path.join(base_dir, 'klbOut_Cam_Long_00258.lux.label.tif')
    output_dir = os.path.join(base_dir, 'test_output')
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    gen_roi(segmented_file, output_dir)

    # Compare the summary file
    file_name = os.path.basename(segmented_file)
    file_prefix = os.path.splitext(file_name)[0]
    summary_file = os.path.join(base_dir, file_prefix + '_summary.csv')
    cmp_summary_file = os.path.join(base_dir, 'compare_' + file_prefix + '_summary.csv')
    assert [row for row in open(summary_file)] == [row for row in open(cmp_summary_file)]
    assert dir_filesize_cmp("data/generate_roi/compare_stardist_rois", "data/generate_roi/test_output") == True


def test_gen_roi_klb():
    base_dir = 'data/generate_roi'
    segmented_file = os.path.join(base_dir, 'klbOut_Cam_Long_00258.lux.label.klb')
    output_dir = os.path.join(base_dir, 'test_output')
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    gen_roi(segmented_file, output_dir)

    # Compare the summary file
    file_name = os.path.basename(segmented_file)
    file_prefix = os.path.splitext(file_name)[0]
    summary_file = os.path.join(base_dir, file_prefix + '_summary.csv')
    cmp_summary_file = os.path.join(base_dir, 'compare_' + file_prefix + '_summary.csv')
    assert [row for row in open(summary_file)] == [row for row in open(cmp_summary_file)]
    assert dir_filesize_cmp("data/generate_roi/compare_stardist_rois", "data/generate_roi/test_output") == True