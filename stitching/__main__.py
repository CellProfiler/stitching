import math
import os
import os.path

import bioformats
import bioformats.formatreader
import click
import javabridge
import javabridge.jutil
import numpy
import numpy.random
import skimage.io
import skimage.util.montage


@click.command()
@click.argument("image", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(exists=False))
@click.option("--image-size", default=55)
@click.option("--montage-size", default=30)


def __main__(image, output, image_size, montage_size):
    try:
        javabridge.start_vm(class_path=bioformats.JARS)

        os.mkdir(output)

        __stitch(image, output, image_size, montage_size)
    finally:
        javabridge.kill_vm()


def __stitch(filename, output, image_size, montage_size):
    reader = bioformats.formatreader.get_image_reader("tmp", path=filename)

    image_count = javabridge.call(reader.metadata, "getImageCount", "()I")

    channel_count = javabridge.call(reader.metadata, "getChannelCount", "(I)I", 0)

    n_chunks = __compute_chunks(image_count/2,montage_size)
    chunk_size = montage_size**2

    for channel in range(channel_count):
        for chunk in range(n_chunks):
            try:
                images = [
                    reader.read(c=channel, series=image) for image in range(image_count)[::2][chunk*chunk_size:(chunk+1)*chunk_size]
                ]
            except javabridge.jutil.JavaException:
                break

            images = [__pad_or_crop(image, image_size) for image in images]

            montage = skimage.util.montage.montage2d(numpy.asarray(images), 0)

            if chunk == (n_chunks-1):
                montage = __pad_to_same_chunk_size(montage, image_size, montage_size)

            skimage.io.imsave(os.path.join(output, "ch{:d}_{:d}.tif".format(channel + 1, chunk + 1)), montage)


def __pad_or_crop(image, image_size):
    bigger = max(image.shape[0], image.shape[1], image_size)

    pad_x = float(bigger - image.shape[0])
    pad_y = float(bigger - image.shape[1])

    pad_width_x = (int(math.floor(pad_x / 2)), int(math.ceil(pad_x / 2)))
    pad_width_y = (int(math.floor(pad_y / 2)), int(math.ceil(pad_y / 2)))
    sample = image[-10:, :10]

    std = numpy.std(sample)

    mean = numpy.mean(sample)

    def normal(vector, pad_width, iaxis, kwargs):
        vector[:pad_width[0]] = numpy.random.normal(mean, std, vector[:pad_width[0]].shape)
        vector[-pad_width[1]:] = numpy.random.normal(mean, std, vector[-pad_width[1]:].shape)
        return vector

    if bigger == image_size:
        return numpy.pad(image, (pad_width_x, pad_width_y), normal)
    else:
        if bigger == image.shape[0]:
            temp_image = numpy.pad(image, (pad_width_y), normal)
        else:
            temp_image = numpy.pad(image, (pad_width_x), normal)
        return temp_image[(bigger - image_size)/2:(bigger + image_size)/2,(bigger - image_size)/2:(bigger + image_size)/2]


def __pad_to_same_chunk_size(small_montage, image_size, montage_size):
    pad_x = float(montage_size*image_size - small_montage.shape[0])

    pad_y = float(montage_size*image_size - small_montage.shape[1])

    npad = ((0,int(pad_y)), (0,int(pad_x)))

    return numpy.pad(small_montage, pad_width=npad, mode='constant', constant_values=0)


def __compute_chunks(n_images, montage_size):

    def remainder(images, groups):
        return (images - groups * (montage_size ** 2))

    n_groups = 1

    while remainder(n_images, n_groups) > 0:
        n_groups += 1

    return n_groups

if __name__ == "__main__":
    __main__()
