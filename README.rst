Stitching
=========

Image stitching


Requirements
============

Python 2.7.12
Pip


Installation
============

Clone this repository

    pip install -e .


Use
===

    python stitching -o OUTPUT_DIRECTORY IMAGE

Generates per-channel tiled images from IMAGE saved to OUTPUT_DIRECTORY. Each image in IMAGE has shape 55px by 55px and
is padded with random noise. Files are named "ch1.tif", "ch2.tif", ..., one for each channel.

    python stitching -o OUTPUT_DIRECTORY --image-size SIZE IMAGE

Generates per-channel tiled images from IMAGE saved to OUTPUT_DIRECTORY. Each image in IMAGE has shape SIZE pixels by
SIZE pixels and is padded with random noise. Files are named "ch1.tif", "ch2.tif", ..., one for each channel.
