from src.roi_convertor.gen_crops import *
import shutil
from test_utils import *


def test_gen_cropbox():
    orig_image_dir = "data/cropping/full_klbs"
    out_crop_dir = "data/cropping/crobpoxes"
    if os.path.isdir(out_crop_dir):
        shutil.rmtree(out_crop_dir)
    os.makedirs(out_crop_dir)
    gen_cropboxes(orig_image_dir, out_crop_dir)

    comparison_dir = "data/cropping/compare_cropboxes"
    dir_filesize_cmp(out_crop_dir, comparison_dir)


def test_gen_crop_tif():
    orig_image_dir = "data/cropping/full_klbs"
    crop_dir = "data/cropping/compare_cropboxes"
    out_image_dir = "data/cropping/tif_crops"
    if os.path.isdir(out_image_dir):
        shutil.rmtree(out_image_dir)
    os.makedirs(out_image_dir)
    generate_crops(orig_image_dir, crop_dir, out_image_dir, 0, 0, 10)

    comparison_dir = "data/cropping/compare_crops_tif"
    dir_filesize_cmp(out_image_dir, comparison_dir)


def test_gen_crop_klb():
    num_threads = 16
    orig_image_dir = "data/cropping/full_klbs"
    crop_dir = "data/cropping/compare_cropboxes"
    out_image_dir = "data/cropping/klb_crops"
    if os.path.isdir(out_image_dir):
        shutil.rmtree(out_image_dir)
    os.makedirs(out_image_dir)
    generate_crops(orig_image_dir, crop_dir, out_image_dir, 0, 0, 10, 150, 0.208, 2, 'klb', False, num_threads)

    comparison_dir = "data/cropping/compare_crops_klb"
    dir_filesize_cmp(out_image_dir, comparison_dir)


def test_gen_crop_mips():
    num_threads = 16
    orig_image_dir = "data/cropping/full_klbs"
    crop_dir = "data/cropping/compare_cropboxes"
    out_image_dir = "data/cropping/mip_crops"
    if os.path.isdir(out_image_dir):
        shutil.rmtree(out_image_dir)
    os.makedirs(out_image_dir)

    visualize_cropboxes(orig_image_dir, crop_dir, out_image_dir, 0, 0, 10, 150, num_threads)

    comparison_dir = "data/cropping/compare_mip_crops"
    dir_filesize_cmp(out_image_dir, comparison_dir)