import click
from time import time
from .gen_rois import gen_roi
from .gen_tif import gen_mask_core
from .gen_diff_rois import check_if_diff
from .gen_analytics import append_hand_correction_guide
from .gen_crops import *
import os
__version__ = "1.1"

@click.group()
@click.version_option(__version__)
def cli():
    pass

@cli.command()
@click.option('--segmentation_image_file',required=True,
              type=click.Path(exists=True,file_okay=True,readable=True),
              help="Segmentation output from Stardist.")
@click.option('--output_dir',required=False,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help="ROI output directory.")
def generate_roi(segmentation_image_file, output_dir):
    click.echo('Invoking ROI generation...')
    t0 = time()
    roi_dir = gen_roi(segmentation_image_file, output_dir)
    t1 = time() - t0
    click.echo('ROIs generated here:' + roi_dir)
    click.echo("Time elapsed: " + str(t1))

@cli.command()
@click.option('--orig_image_dir',required=True,
              type=click.Path(exists=True,file_okay=False,dir_okay=True,readable=True),
              help="Original klb/tif/h5/npy files.")
@click.option('--output_dir',required=True,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help="Output directory to save the crops.")
@click.option("--timestamp_min","-tb", required=False, default=0, type=click.INT,
            help="The first timestamp to use for cropping.")
@click.option("--timestamp_max","-te", required=False, default=-1, type=click.INT,
            help="The last timestamp to use for cropping. Setting -1 means use to the last available.")
@click.option("--generate_plots", required=False, type=click.Choice(["True", "False"]),
              help="Generate cropping plots.", default="False")
@click.option("--filter_window_size","-ws", required=False, default=100, type=click.FLOAT, show_default=True,
            help="The size of the uniform filter applied to the images.")
@click.option("--filter_threshold","-thresh", required=False, default=0.1, type=click.FLOAT, show_default=True,
            help="The thresholding applied to the image after the uniform filtering.")
def generate_cropboxes(orig_image_dir, output_dir, timestamp_min, timestamp_max,
                  generate_plots, filter_window_size, filter_threshold):

    click.echo('Invoking crop box generation...')
    t0 = time()
    box_count = gen_cropboxes(orig_image_dir, output_dir, timestamp_min, timestamp_max,
                  generate_plots, filter_window_size, filter_threshold)
    t1 = time() - t0

    click.echo('Crop boxes generated. Number of boxes: ' + str(box_count))
    if box_count == 0:
        click.echo('ERROR!!! No crop boxes found. Adjust timestamps.')
    elif box_count > 1:
        click.echo('WARNING!!! Multiple crop boxes found. Need to select one for membrane cropping.')

    click.echo("Time elapsed: " + str(t1))

@cli.command()
@click.option('--orig_image_dir',required=True,
              type=click.Path(exists=True,file_okay=False,dir_okay=True,readable=True),
              help="Original klb/tif/h5/npy files.")
@click.option('--crop_file_dir',required=True,
              type=click.Path(exists=True,file_okay=False,dir_okay=True,readable=True),
              help="The directory with hpair.csv and vpair.csv generated with generate-cropboxes.")
@click.option("--cropbox_index","-cbi", required=False, default=0, type=click.INT, show_default=True,
              help="The cropbox to visualize for cropping.")
@click.option('--output_dir',required=True,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help="Output directory to save the crops.")
@click.option('--output_format','-f', required=False, default="klb", type=click.Choice(['klb','h5','tif','npy']),
              help='The output format klb/h5/tif/npy.')
@click.option("--timestamp_min","-tb", required=False, default=0, type=click.INT, show_default=True,
              help="The first timestamp to use for cropping.")
@click.option("--timestamp_max","-te", required=False, default=-1, type=click.INT, show_default=True,
              help="The last timestamp to use for cropping. Setting -1 means use to the last available.")
@click.option("--offset","-of", required=False, default=150, type=click.INT, show_default=True,
              help="The offset used during cropping.")
@click.option("--x_y_scaling","-x_y_sc", required=False, default=0.208, type=click.FLOAT, show_default=True,
              help="The multiple used for X and Y axis scaling.")
@click.option("--z_scaling","-z_sc", required=False, default=2, type=click.FLOAT, show_default=True,
              help="The multiple used for Z axis scaling.")
def crop_images(orig_image_dir, crop_file_dir, cropbox_index, output_dir, output_format,
                timestamp_min, timestamp_max, offset, x_y_scaling, z_scaling):
    click.echo('Cropping images...')
    t0 = time()
    generate_crops(orig_image_dir, crop_file_dir, output_dir, cropbox_index, timestamp_min,
                   timestamp_max, offset, x_y_scaling, z_scaling, output_format)
    t1 = time() - t0
    click.echo('Cropped files generated here:' + output_dir)
    click.echo("Time elapsed: " + str(t1))

@cli.command()
@click.option('--orig_image_dir',required=True,
              type=click.Path(exists=True,file_okay=False,dir_okay=True,readable=True),
              help="Original klb/tif/h5/npy files.")
@click.option('--crop_file_dir',required=True,
              type=click.Path(exists=True,file_okay=False,dir_okay=True,readable=True,writable=True),
              help="The directory with hpair.csv and vpair.csv generated with generate-cropboxes.")
@click.option("--cropbox_index","-cbi", required=True, type=click.INT,
              help="The cropbox to visualize for cropping.")
@click.option("--timestamp_min","-tb", required=False, default=0, type=click.INT,
              help="The first timestamp to use for cropping.")
@click.option("--timestamp_max","-te", required=False, default=-1, type=click.INT,
              help="The last timestamp to use for cropping. Setting -1 means use to the last available.")
@click.option("--offset","-of", required=False, default=150, type=click.INT,
              help="The offset used during cropping.")
def visualize_crops(orig_image_dir, crop_file_dir, cropbox_index, timestamp_min, timestamp_max, offset):
    click.echo('Generating cropped MIP images...')
    t0 = time()
    visualize_cropboxes(orig_image_dir, crop_file_dir, cropbox_index, timestamp_min, timestamp_max, offset)
    t1 = time() - t0
    click.echo('Cropped MIPs generated here:' + crop_file_dir)
    click.echo("Time elapsed: " + str(t1))

@cli.command()
@click.option('--orig_image', required=True,
              type=click.Path(exists=True,file_okay=True,dir_okay=True,readable=True),
              help= "Original image file or directory with the files.")
@click.option('--roi_dir', required=False,
              type=click.Path(exists=True,dir_okay=True,file_okay=False,readable=True),
              help= "Directory with ROI files. The files must be named as <orig_file_name>_<slice_id>.zip")
@click.option('--output_dir', required=False,
              type=click.Path(exists=True,dir_okay=True,file_okay=False,readable=True),
              help= "Output directory to save the segmentation mask output.")
@click.option("--output_format", required=False, default="tif",
    type=click.Choice(["klb","h5","tif","npy"]),
    help="The output format klb/h5/tif/npy.")
def generate_mask(orig_image, roi_dir, output_dir, output_format):
    click.echo('Invoking mask generation...')
    t0 = time()
    if output_dir and roi_dir and os.path.isdir(roi_dir) and os.path.isdir(output_dir):
        if os.path.isdir(orig_image):
            result = [os.path.join(dp, f)
                      for dp, dn, filenames in os.walk(orig_image)
                      for f in filenames if (os.path.splitext(f)[1] == '.klb' or
                                             os.path.splitext(f)[1] == '.h5' or
                                             os.path.splitext(f)[1] == '.tif' or
                                             os.path.splitext(f)[1] == '.npy')]
            for image_file in result:
                print("Processing image:", image_file)
                file_name = os.path.basename(image_file)
                file_prefix = os.path.splitext(file_name)[0]
                file_ext = os.path.splitext(file_name)[1]
                hand_corrected_tif = gen_mask_core(roi_dir, image_file, output_dir, output_format)
                click.echo('Hand corrected mask generated:' + hand_corrected_tif)
        else:
            hand_corrected_tif = gen_mask_core(roi_dir, orig_image, output_dir, output_format)
            click.echo('Hand corrected mask generated:' + hand_corrected_tif)
    else:
        if os.path.isdir(orig_image):
            roi_dir = os.path.join(orig_image, "stardist_rois")
            result = [os.path.join(dp, f)
                      for dp, dn, filenames in os.walk(orig_image)
                      for f in filenames if (os.path.splitext(f)[1] == '.klb' or
                                             os.path.splitext(f)[1] == '.h5' or
                                             os.path.splitext(f)[1] == '.tif' or
                                             os.path.splitext(f)[1] == '.npy')]
            for image_file in result:
                print("Processing image:", image_file)
                file_name = os.path.basename(image_file)
                file_prefix = os.path.splitext(file_name)[0]
                file_ext = os.path.splitext(file_name)[1]
                hand_corrected_tif = gen_mask_core(roi_dir, image_file, orig_image, output_format)
                click.echo('Hand corrected mask generated:' + hand_corrected_tif)
        else:
            base_dir = os.path.dirname(orig_image)
            roi_dir = os.path.join(base_dir, "stardist_rois")
            hand_corrected_tif = gen_mask_core(roi_dir, orig_image, base_dir, output_format)
            click.echo('Hand corrected mask generated:' + hand_corrected_tif)
    t1 = time() - t0
    click.echo("Time elapsed: " + str(t1))

@cli.command()
@click.option('--orig_image', required=True,
              type=click.Path(exists=True,file_okay=True,dir_okay=True,readable=True),
              help= "Original image file or directory.")
@click.option('--segmentation_image',required=True,
              type=click.Path(exists=True,file_okay=True,dir_okay=True,readable=True),
              help="Segmentation output fire or directory from inference.")
@click.option('--output_file', required=True,
              type=click.Path(exists=False,dir_okay=False,file_okay=True),
              help= "Output file name.")
@click.option("--check_fn","-cfn", is_flag=True,
    help="Run false negative detection.", default = False)
def generate_analytics(orig_image, segmentation_image, output_file, check_fn):
    click.echo('Invoking analytics generation...')
    t0 = time()
    if os.path.isdir(orig_image) and os.path.isdir(segmentation_image):
        result = [os.path.join(dp, f)
                  for dp, dn, filenames in os.walk(orig_image)
                  for f in filenames if (os.path.splitext(f)[1] == '.klb' or
                                         os.path.splitext(f)[1] == '.h5' or
                                         os.path.splitext(f)[1] == '.tif' or
                                         os.path.splitext(f)[1] == '.npy')]
        for image_file in result:
            print("Processing image:", image_file)
            file_name = os.path.basename(image_file)
            file_prefix = os.path.splitext(file_name)[0]
            file_ext = os.path.splitext(file_name)[1]
            segmentation_image_file = os.path.join(segmentation_image,file_prefix + ".label" + file_ext)
            segmentation_image_file_corrected = os.path.join(segmentation_image,file_prefix + "_SegmentationCorrected" + file_ext)
            if os.path.isfile(segmentation_image_file):
                append_hand_correction_guide(segmentation_image_file, image_file, output_file, check_fn)
            elif os.path.isfile(segmentation_image_file_corrected):
                append_hand_correction_guide(segmentation_image_file_corrected, image_file, output_file, check_fn)
            else:
                click.echo('Segmentation output not found. Expected file:' + segmentation_image_file)
    elif os.path.isfile(orig_image) and os.path.isfile(segmentation_image):
        append_hand_correction_guide(segmentation_image, orig_image, output_file, check_fn)
    else:
        click.echo('Please provide either input files or directories, combinations are not supported.')
    t1 = time() - t0
    click.echo('Analytics file generated:' + output_file)
    click.echo("Time elapsed: " + str(t1))

@cli.command()
@click.option('--orig_roi_dir', required=True,
              type=click.Path(exists=True,file_okay=False,dir_okay=True,readable=True),
              help= "ROI directory generated from segmentation.")
@click.option('--corrected_roi_dir',required=True,
              type=click.Path(exists=True,file_okay=False,dir_okay=True,readable=True),
              help="ROI directory edited by hand correction.")
def roi_diff(orig_roi_dir, corrected_roi_dir):
    click.echo('Invoking diff generation...')
    t0 = time()
    orig_zf_list = []
    for zf in os.listdir(orig_roi_dir):
        if zf.endswith('.zip'):
            orig_zf_list.append(zf)

    corrected_zf_list = []
    for zf in os.listdir(corrected_roi_dir):
        if zf.endswith('.zip'):
            corrected_zf_list.append(zf)

    zdir_only_orig = list(set(orig_zf_list)-set(corrected_zf_list))
    zdir_only_corrected = list(set(corrected_zf_list)-set(orig_zf_list))

    zdir_common = set(orig_zf_list).intersection(set(corrected_zf_list))

    # File level diff
    diff_list = []
    for only_file in zdir_only_orig:
        diff_list.append(only_file + ',' + 'Present' + ',' + 'Absent')
    for only_file in zdir_only_corrected:
        diff_list.append(only_file + ',' + 'Absent' + ',' + 'Present')

    for common_file in zdir_common:
        is_diff, orig_only, corrected_only = check_if_diff(os.path.join(orig_roi_dir,common_file),
                   os.path.join(corrected_roi_dir,common_file))
        if is_diff:
            orig_only_labels = "|".join(os.path.splitext(roi_name)[0] for roi_name in orig_only)
            corrected_only_labels = "|".join(os.path.splitext(roi_name)[0] for roi_name in corrected_only)
            diff_list.append(common_file + ',' + orig_only_labels + ',' + corrected_only_labels)

    if diff_list:
        output_file = "diff_report.csv"
        click.echo("Differences found! Report: {0}".format(output_file))
        with open(output_file,'w') as f_out:
            f_out.write('ROI_file,Oiginal ROI Set,Corrected ROI Set\n')
            for line in diff_list:
                f_out.write(line + '\n')
    else:
        click.echo("No Differences found!")

    t1 = time() - t0
    click.echo("Time elapsed: " + str(t1))

def main():
    cli()
