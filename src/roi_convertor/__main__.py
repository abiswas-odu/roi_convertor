import click
from time import time
from .gen_rois import gen_roi
from .gen_tif import gen_tif, gen_mask_core
import os
__version__ = "0.4a"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--orig_image_file',required=True,
              type=click.Path(exists=True,file_okay=True,readable=True),
              help="Segmentation output from Stardist.")
@click.option('--output_dir',required=False,
              type=click.Path(exists=True,dir_okay=True,readable=True),
              help="ROI output directory.")
def generate_roi(orig_image_file, output_dir):
    click.echo('Invoking ROI generation...')
    t0 = time()
    roi_dir = gen_roi(orig_image_file, output_dir)
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
        hand_corrected_tif = gen_tif(orig_image_file)
    t1 = time() - t0
    click.echo('Hand corrected mask generated:' + hand_corrected_tif)
    click.echo("Time elapsed: " + str(t1))

def main():
    cli()
