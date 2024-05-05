# Python JPEG Image Recovery Script
This script can be used to extract JPEG images from corrupted binary file (this can be binary data of corrupted hard drive). It scans the file byte by byte and tries to find JPEG specific header. Once found, it collects image data until it finds JPEG ending sequence, after which it continues scanning for more images.

## Usage
- Paste main.py into folder where result images should be saved.
- Open SHELL and navigate into this folder.
- Run command `python main.py <path_to_binary_file> <info_frequency>`.

You will be informed about progress after each info_frequency of MBs processed. When finished, you will be informed about scanning speed (our top speed during testing was about 1.15 MB/s). Found image is dumped into script folder as soon as it is completed, meaning that images are saved during script runtime.

## Hear me out
The script is pretty dumb and is not refactored as it is a result of less than an hour of coding and debugging, since it was created during Forensic Analysis laboratory.