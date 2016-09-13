import bioformats
import javabridge
import math
import numpy


def __get_image(reader, image_number, channel):
    javabridge.call(reader, "setSeries", "(I)V", image_number)

    index = javabridge.call(reader, "getIndex", "(III)I", 0, channel, 0)

    bytes = javabridge.call(reader, "openBytes", "(I)[B", index)

    pixel_type = javabridge.call(reader, "getPixelType", "()I")

    pixels = javabridge.static_call(
        "loci/common/DataTools",
        "makeDataArray",
        "([BIZZ)Ljava/lang/Object;",
        bytes,
        javabridge.static_call("loci/formats/FormatTools", "getBytesPerPixel", "(I)I", pixel_type),
        javabridge.static_call("loci/formats/FormatTools", "isFloatingPoint", "(I)Z", pixel_type),
        javabridge.call(reader, "isLittleEndian", "()Z")
    )

    n_pixels = javabridge.static_call("java/lang/reflect/Array", "getLength", "(Ljava/lang/Object;)I", pixels)

    # TODO: cast from Object to short[] (or Object to Short[] to short[])
    image = [
        javabridge.static_call(
            "java/lang/reflect/Array",
            "getShort",
            "(Ljava/lang/Object;I)S",
            pixels,
            pixel
        ) for pixel in range(n_pixels)
    ]

    width = javabridge.call(reader, "getSizeX", "()I")

    height = javabridge.call(reader, "getSizeY", "()I")

    return numpy.asarray(image).reshape(height, width)


def __pad_image(image, dim_x, dim_y):
    pad_x = float(dim_x - image.shape[0])

    pad_y = float(dim_y - image.shape[1])

    pad_width_x = (int(math.floor(pad_x / 2)), int(math.ceil(pad_x / 2)))

    pad_width_y = (int(math.floor(pad_y / 2)), int(math.ceil(pad_y / 2)))

    return numpy.pad(image, (pad_width_x, pad_width_y), 'constant', constant_values=0)


def montage():
    javabridge.start_vm(class_path=bioformats.JARS)

    fname = "/Users/mcquin/Downloads/cif_reader_implementation/testfile_CRF118_Eosinophil_small.cif"

    image_size = 55

    grid_size = 33

    reader = javabridge.make_instance(
        "loci/formats/ChannelSeparator",
        "(Lloci/formats/IFormatReader;)V",
        javabridge.make_instance("loci/formats/ChannelFiller", "()V")
    )

    omexml = javabridge.make_instance("loci/formats/services/OMEXMLServiceImpl", "()V")

    javabridge.call(
        reader,
        "setMetadataStore",
        "(Lloci/formats/meta/MetadataStore;)V",
        javabridge.call(omexml, "createOMEXMLMetadata", "()Lloci/formats/ome/OMEXMLMetadata;")
    )

    javabridge.call(reader, "setId", "(Ljava/lang/String;)V", fname)

    metadata = javabridge.call(reader, "getMetadataStore", "()Lloci/formats/meta/MetadataStore;")

    n_images = javabridge.call(metadata, "getImageCount", "()I")

    n_channels = javabridge.call(metadata, "getChannelCount", "(I)I", 0)

    for channel in range(n_channels):

        montage = numpy.zeros((grid_size * image_size, grid_size * image_size))

        for image in range(n_images):

            pixels = __pad_image(__get_image(reader, image, channel), image_size, image_size)

            x_start = (image / 2) % grid_size * image_size

            x_end = x_start + image_size

            y_start = (image / 2) / grid_size * image_size

            y_end = y_start + image_size

            montage[x_start:x_end, y_start:y_end] = pixels

            if image / 2 == grid_size**2 - 1:
                # save montage

                montage = numpy.zeros((grid_size * image_size, grid_size * image_size))

        # save montage

    javabridge.kill_vm()


if __name__ == '__main__':
    montage()
