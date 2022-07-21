import click
from time import time
from .gen_rois import gen_roi
from .gen_tif import gen_mask_core
from .gen_analytics import append_hand_correction_guide
import os
__version__ = "0.6a"

@click.group()
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
@click.option('--orig_image_file', required=True,
              type=click.Path(exists=True,file_okay=True,readable=True),
              help= "Original image file or segmentation output.")
@click.option('--roi_dir', required=False,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help= "Directory with ROI files. The files must be named as <orig_file_name>_<slice_id>.zip")
@click.option('--output_dir', required=False,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help= "Output directory to save the segmentation mask output.")
@click.option("--output_format", required=False, default="tif",
    type=click.Choice(["klb","h5","tif","npy"]),
    help="The output format klb/h5/tif/npy.")
def generate_mask(orig_image_file, roi_dir, output_dir, output_format):
    click.echo('Invoking mask generation...')
    t0 = time()
    if output_dir and roi_dir and os.path.isdir(roi_dir) and os.path.isdir(output_dir):
        hand_corrected_tif = gen_mask_core(roi_dir, orig_image_file, output_dir, output_format)
    else:
        base_dir = os.path.dirname(orig_image_file)
        roi_dir = os.path.join(base_dir, "stardist_rois")
        hand_corrected_tif = gen_mask_core(roi_dir, orig_image_file, base_dir, output_format)
    t1 = time() - t0
    click.echo('Hand corrected mask generated:' + hand_corrected_tif)
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
            if os.path.isfile(segmentation_image_file):
                append_hand_correction_guide(segmentation_image_file, image_file, output_file, check_fn)
            else:
                click.echo('Segmentation output not found. Expected file:' + segmentation_image_file)
    elif os.path.isfile(orig_image) and os.path.isfile(segmentation_image):
        append_hand_correction_guide(segmentation_image, orig_image, output_file, check_fn)
    else:
        click.echo('Please provide either input files or directories, combinations are not supported.')
    t1 = time() - t0
    click.echo('Analytics file generated:' + output_file)
    click.echo("Time elapsed: " + str(t1))

def main():
    cli()
