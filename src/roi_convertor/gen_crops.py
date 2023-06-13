from .io_utils import *
import os
import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import pandas as pd
from skimage.transform import rescale
from PIL import Image

def to_even(x):
    return 2*int(round(x/2))


def gen_cropboxes(orig_image_dir, out_dir, time_min=0, time_max=-1, plot=True,
                  filter_window_size=100, threshold_after_filter=0.1, num_threads: int = 1):
    vpairs_potential = {}
    vpairs = {}
    hpairs = {}
    num_boxes = {}
    all_ims = []
    images = [os.path.join(dp, f)
              for dp, dn, filenames in os.walk(orig_image_dir)
              for f in filenames if (os.path.splitext(f)[1] == '.klb' or
                                     os.path.splitext(f)[1] == '.h5' or
                                     os.path.splitext(f)[1] == '.tif' or
                                     os.path.splitext(f)[1] == '.npy')]
    if time_max == -1:
        time_max = len(images) - 1

    # Sort images in order of timestamp
    images = np.sort(images)

    # Check if some images are found
    if len(images) == 0:
        raise ValueError('No images found to generate cropboxes for.')

    # Generate a sum of images by loading the first one to get the shape an initialize the sum array
    image = read_image(str(images[0]), num_threads)
    sum_of_images = np.zeros(image.shape)
    for im in images[time_min:time_max+1]:
        print('Processing:', str(im), flush=True)
        a = read_image(str(im), num_threads)
        corrected = a[:,:,:].astype('float64')-a[-1,:,:].astype('float64')
        sum_of_images = sum_of_images + corrected

    # Compute the average of the image
    corrected = sum_of_images / len(images[time_min:time_max+1])

    # sm1 = ndimage.uniform_filter(corrected.mean(1).mean(0), filter_window_size)
    sm2 = ndimage.uniform_filter(corrected.mean(2).mean(0), filter_window_size)
    if plot:
        plt.figure()
        plt.plot(sm2/max(sm2))
        plt.axhline(threshold_after_filter)
        if os.path.exists(os.path.join(out_dir,"crop.png")):
            os.remove(os.path.join(out_dir,"crop.png"))
        plt.savefig(os.path.join(out_dir,"crop.png"))
        plt.close()
    vboxes = (sm2 / max(sm2) > threshold_after_filter).astype(int)
    vboxes = np.concatenate([[0], vboxes])
    vboxes = np.concatenate([vboxes, [0]])
    bndrs = np.where((vboxes[1:] - vboxes[:-1])!=0)[0]

    if len(bndrs) % 2 != 0:
        raise ValueError('Something wrong with boundaries. Inspect plot.')
    else:
        num_boxes['all'] = len(bndrs) // 2
    vpairs_potential['all'] = [(to_even(bndrs[2*k]), to_even(bndrs[2*k+1])) for k in range(num_boxes['all'])]
    vpairs['all'] = []
    hpairs['all'] = []
    found_pair_index = 0
    for index, pair in enumerate(vpairs_potential['all']):
        try:
            if pair[0] < pair[1]: # The pairs are not wrong way round or equal
                sm = ndimage.uniform_filter(corrected.mean(0)[pair[0]:pair[1],:].mean(0), filter_window_size)
                hbox = (sm / max(sm) > threshold_after_filter).astype(int)
                hbox = np.concatenate([[0], hbox])
                hbox = np.concatenate([hbox, [0]])
                bndrs = np.where((hbox[1:] - hbox[:-1])!=0)[0]
                hpairs['all'].append((to_even(bndrs[0]), to_even(bndrs[1])))
                vpairs['all'].append(pair)
                if plot:
                    plt.figure()
                    plt.plot(sm/max(sm))
                    plt.axhline(threshold_after_filter)
                    if os.path.exists(os.path.join(out_dir,'crop_' + str(found_pair_index) + '.png')):
                        os.remove(os.path.join(out_dir,'crop_' + str(found_pair_index) + '.png'))
                    plt.savefig(os.path.join(out_dir,'crop_' + str(found_pair_index) + '.png'))
                    plt.close()
                found_pair_index = found_pair_index + 1
        except Exception as e:
            print('Cropbox generation produced and error:', e)

    vpairs = pd.DataFrame(vpairs)
    hpairs = pd.DataFrame(hpairs)
    vpairs.to_csv(os.path.join(out_dir, 'vpairs.csv'))
    hpairs.to_csv(os.path.join(out_dir, 'hpairs.csv'))

    return num_boxes['all']


def visualize_cropboxes(orig_image_dir: os.PathLike, crop_dir: os.PathLike, output_dir: os.PathLike,
 cropbox_index: int, time_min:int = 0, time_max: int = -1, offset:int = 150, num_threads: int = 1):
    try:
        vpairs = pd.read_csv(os.path.join(crop_dir, 'vpairs.csv'), index_col=[0])
        hpairs = pd.read_csv(os.path.join(crop_dir, 'hpairs.csv'), index_col=[0])

        vpairs = tuple(map(int, vpairs['all'][cropbox_index][1:-1].split(', ')))
        hpairs = tuple(map(int, hpairs['all'][cropbox_index][1:-1].split(', ')))
        crop_x_min = max(hpairs[0]-offset,0)
        crop_x_max = min(hpairs[1]+offset, 2048)
        crop_y_min = max(vpairs[0]-offset,0)
        crop_y_max = min(vpairs[1]+offset, 2048)

        images = [os.path.join(dp, f)
                  for dp, dn, filenames in os.walk(orig_image_dir)
                  for f in filenames if (os.path.splitext(f)[1] == '.klb' or
                                         os.path.splitext(f)[1] == '.h5' or
                                         os.path.splitext(f)[1] == '.tif' or
                                         os.path.splitext(f)[1] == '.npy')]
        if time_max == -1:
            time_max = len(images) - 1

        # Sort images in order of timestamp
        images = np.sort(images)
        for im in images[time_min:time_max + 1]:
            image_file = str(im)
            print('Processing:', image_file, flush=True)
            a = read_image(image_file, num_threads)
            file_base = os.path.basename(image_file).split(os.extsep)
            timepoint = file_base[0].split('_')[-1]
            cropped_mip = np.array(a).max(0)[crop_y_min:crop_y_max, crop_x_min:crop_x_max]
            # Prodice the MIP in png format
            mip_to_file = os.path.join(output_dir, file_base[0] + '_crop_MIP.png')
            mipOut = np.ascontiguousarray(cropped_mip)
            mipIMG = Image.fromarray(mipOut)
            mipIMG.save(mip_to_file)
    except Exception as e:
        print('Cropbox visualization produced and error:', e)


def generate_crops(image_dir: str, crop_dir: str, output_dir: str, cropbox_index,
                   time_min: int = 0, time_max: int = -1, offset: int = 0,
                   x_y_sc: float = 0.208, z_sc: float = 2, output_format: str = 'tif',
                   do_rescale: bool = True, num_threads: int = 1):
    try:
        vpairs = pd.read_csv(os.path.join(crop_dir, 'vpairs.csv'), index_col=[0])
        hpairs = pd.read_csv(os.path.join(crop_dir, 'hpairs.csv'), index_col=[0])

        vpairs = tuple(map(int, vpairs['all'][cropbox_index][1:-1].split(', ')))
        hpairs = tuple(map(int, hpairs['all'][cropbox_index][1:-1].split(', ')))
        crop_x_min = max(hpairs[0]-offset,0)
        crop_x_max = min(hpairs[1]+offset, 2048)
        crop_y_min = max(vpairs[0]-offset,0)
        crop_y_max = min(vpairs[1]+offset, 2048)

        images = [os.path.join(dp, f)
                  for dp, dn, filenames in os.walk(image_dir)
                  for f in filenames if (os.path.splitext(f)[1] == '.klb' or
                                         os.path.splitext(f)[1] == '.h5' or
                                         os.path.splitext(f)[1] == '.tif' or
                                         os.path.splitext(f)[1] == '.npy')]
        if time_max == -1:
            time_max = len(images) - 1

        # Sort images in order of timestamp
        images = np.sort(images)
        for im in images[time_min:time_max + 1]:
            image_file = str(im)
            print('Processing:', image_file, flush=True)
            a = read_image(image_file, num_threads)
            cur_box = a[:, crop_y_min:crop_y_max, crop_x_min:crop_x_max]
            file_base = os.path.basename(image_file).split(os.extsep)
            if do_rescale:
                cur_box_resc_low = rescale(cur_box,
                                       (1/(2*x_y_sc), 1/(2*z_sc), 1/(2*z_sc)),
                                       preserve_range = True,
                                       anti_aliasing = True)
                write_image(cur_box_resc_low, os.path.join(output_dir, file_base[0] + '.crop'), output_format)
            else:
                cur_box = np.ascontiguousarray(cur_box)
                write_image(cur_box, os.path.join(output_dir, file_base[0] + '.crop'), output_format)
    except Exception as e:
        print('Cropbox visualization produced and error:', e)


def rescale_all_images(image_dir: str, output_dir: str, time_min: int = 0, time_max: int = -1,
                   x_y_sc: float = 0.208, z_sc: float = 2, output_format: str = 'tif', num_threads: int = 1):
    try:
        images = [os.path.join(dp, f)
                  for dp, dn, filenames in os.walk(image_dir)
                  for f in filenames if (os.path.splitext(f)[1] == '.klb' or
                                         os.path.splitext(f)[1] == '.h5' or
                                         os.path.splitext(f)[1] == '.tif' or
                                         os.path.splitext(f)[1] == '.npy')]
        if time_max == -1:
            time_max = len(images) - 1

        # Sort images in order of timestamp
        images = np.sort(images)
        for im in images[time_min:time_max + 1]:
            image_file = str(im)
            print('Processing:', image_file, flush=True)
            a = read_image(image_file, num_threads)
            file_base = os.path.basename(image_file).split(os.extsep)
            cur_box_resc_low = rescale(a, (1/(2*x_y_sc), 1/(2*z_sc), 1/(2*z_sc)),
                                       preserve_range = True,
                                       anti_aliasing = True)
            write_image(cur_box_resc_low, os.path.join(output_dir, file_base[0] + '.rescale'), output_format)
    except Exception as e:
        print('Rescaling produced and error:', e)