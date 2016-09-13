import math
import os
import os.path

import bioformats
import bioformats.formatreader
import click
import javabridge
import numpy
import numpy.random
import skimage.io
import skimage.util.montage


@click.command()
@click.argument("image", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(exists=False))
@click.option("--image-size", default=55)
def __main__(image, output, image_size):
    try:
        javabridge.start_vm(class_path=bioformats.JARS)

        os.mkdir(output)

        __stitch(image, output, image_size)
    finally:
        javabridge.kill_vm()


def __stitch(filename, output, image_size):
    reader = bioformats.formatreader.get_image_reader("tmp", path=filename)

    n_images = javabridge.call(reader.metadata, "getImageCount", "()I")

    n_channels = javabridge.call(reader.metadata, "getChannelCount", "(I)I", 0)

    for channel in range(n_channels):
        images = [__pad(reader.read(c=channel, series=image), image_size) for image in range(n_images)[::2]]

        montage = skimage.util.montage.montage2d(numpy.asarray(images), 0)

        skimage.io.imsave(os.path.join(output, "ch{:d}.tif".format(channel + 1)), montage)


def __pad(image, image_size):
    pad_x = float(image_size - image.shape[0])

    pad_y = float(image_size - image.shape[1])

    pad_width_x = (int(math.floor(pad_x / 2)), int(math.ceil(pad_x / 2)))

    pad_width_y = (int(math.floor(pad_y / 2)), int(math.ceil(pad_y / 2)))

    sample = image[-10:, :10]

    std = numpy.std(sample)

    mean = numpy.mean(sample)

    def normal(vector, pad_width, iaxis, kwargs):
        vector[:pad_width[0]] = numpy.random.normal(mean, std, vector[:pad_width[0]].shape)

        vector[-pad_width[1]:] = numpy.random.normal(mean, std, vector[-pad_width[1]:].shape)

        return vector

    return numpy.pad(image, (pad_width_x, pad_width_y), normal)


if __name__ == "__main__":
    __main__()
