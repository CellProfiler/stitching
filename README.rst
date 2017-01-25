Stitching
=========

Stitch images to form a montage. A montage contains of a n-by-n grid, where in each grid compartment an image can be placed, e.g., a 5-by-5 montage contains 25 images in total. Visit http://cellprofiler.org/imagingflowcytometry/ for more information on the imaging flow cytometry workflow and the image stitching (also referred to as image tiling).

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

Tkinter
  typically included with your python distribution

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
Generates per-channel montages from IMAGE saved to OUTPUT_DIRECTORY. Each image in IMAGE has shape 55px by 55px and is padded with random noise. Montage files are named "ch1.tif", "ch2.tif", ..., one for each channel.

Open a new command line window (also called command prompt window in Windows OS or terminal in MAC OS). Now, to generate the montages, you can either (1) start the stitching GUI or (2) use the command line.

1. To use the GUI, type
  $ python stitching
The GUI window will open where you can select a .cif file to generate the montages. Optionally you can also display selected images from the .cif file.

OR

2. To use the command line, type
  $ python stitching -image='path/to/IMAGE' -output='path/to/OUTPUT_DIRECTORY'


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
