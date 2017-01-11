Stitching
=========

Stitch images to form a montage.

Requirements
============

Java development kit

Python 2.7.12

pip

numpy
  $ pip install numpy

scipy
  $ pip install scipy

click
  $ pip install click

skimage
  $ pip install skimage

python-bioformats
  $ pip install python-bioformats

matplotlib
  $ pip install matplotlib

Additional in Windows OS: Visual C++ 9.0

Installation
============

  $ git clone https://github.com/CellProfiler/stitching.git

  $ cd /path/to/stitching

  $ pip install -e .

Use
===

  $ python stitching -o path/to/OUTPUT_DIRECTORY path/to/IMAGE

Generates per-channel tiled images from IMAGE saved to OUTPUT_DIRECTORY. Each image in IMAGE has shape 55px by 55px and
is padded with random noise. Files are named "ch1.tif", "ch2.tif", ..., one for each channel.

Optional:

--image-size
    Set the window size of the tile images (default: --image-size 55).
    If user sets a size bigger than the original images, each of the tile images will be padded with its own background.
    If user sets a size smaller than the original images, each of the tile images will be cropped toward its center.
--montage-size
    Set the size of the final montage (default: --montage-size 30).
    If the total number of original images could not fill up the desired montage size, the montage will be padded with black background.
      For example:

      Number of total images: 1000

      User setting: --image-size 20 --montage-size 30

      The result would be 2 montages at the size of 600x600; one montage is filled up with 900 (30x30) tile images, one montage contains 100 tile images and remaining space is filled up by black background.
