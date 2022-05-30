import click
import logging
from time import time
import os
from roi_convertor.gen_rois import gen_roi
from roi_convertor.gen_tif import gen_tif

__version__ = "1.0"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--segmentation_mask',required=True,
              type=click.Path(exists=True,file_okay=True,readable=True),
              help="Segmentation output from Stardist.")
def generate_roi(segmentation_mask):
    click.echo('Invoking ROI generation...')
    t0 = time()
    roi_dir = gen_roi(segmentation_mask)
    t1 = time() - t0
    click.echo('ROIs generated here:' + roi_dir)
    click.echo("Time elapsed: " + str(t1))

@cli.command()
@click.option('--segmentation_mask', required=True,
              type=click.Path(exists=True,file_okay=True,readable=True),
              help= "Segmentation output from Stardist.")
def generate_mask(segmentation_mask):
    click.echo('Invoking mask generation...')
    t0 = time()
    hand_corrected_tif = gen_tif(segmentation_mask)
    t1 = time() - t0
    click.echo('Hand corrected mask generated:' + hand_corrected_tif)
    click.echo("Time elapsed: " + str(t1))

def main():
    cli()
