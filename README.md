# Preprocessing - Longitudinal Multipel Sclerosis Lesion Segmentation Challenge - MICCAI21

Data preprocessing for the Longitudinal Multipel Sclerosis Lesion Segmentation Challenge of MICCAI 2021.

The preprocessing consists in three steps:
 - brain extraction
 - bias correction
 - crop

This project uses [anima](https://anima.irisa.fr/) to preprocess the data.

## Installation

 1. Download the Anima Binaries [from the download page](https://anima.irisa.fr/downloads/)
 1. Clone the [Anima Scripts Public repository](https://github.com/Inria-Visages/Anima-Scripts-Public)
 1. Clone the [Anima Scripts Public Data repository](https://github.com/Inria-Visages/Anima-Scripts-Data-Public/) containing the template used for the brain extraction
 1. Create the `~/.anima/config.txt` file to configure anima, containing the following paths:
 

```
# Variable names and section titles should stay the same
# Put this file in your HomeFolder/.anima/config.txt
# Make the anima variable point to your Anima public build
# Make the extra-data-root point to the data folder of Anima-Scripts
# The last folder separator for each path is crucial, do not forget them
# Use full paths, nothing relative or using tildes 

[anima-scripts]
anima-scripts-public-root = /path/to/Anima-Scripts-Public/
anima = /path/to/Anima-Binaries/
extra-data-root = /path/to/Anima-Scripts-Data-Public/
```

## Usage

```
preprocess.py [-h] -i INPUT -o OUTPUT [-a ANIMA]
                     [-s ANIMA_SCRIPTS_PUBLIC]

Preprocess data from the Longitudinal MS Lesion Segmentation Challenge of
MICCAI 2021 with the anima library. The preprocessing consists in a brain
extraction followed by a bias field correction.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input folder containing the patients to preprocess
                        (for example
                        segmentation_challenge_miccai21/training/).
  -o OUTPUT, --output OUTPUT
                        Output folder where the processed data will be saved
                        (it will follow the same file structure as the input
                        folder).
  -a ANIMA, --anima ANIMA
                        The directory containing the anima binaries (optional,
                        the script will look for this information in the
                        ~/.anima/config.txt file by default).
  -s ANIMA_SCRIPTS_PUBLIC, --anima_scripts_public ANIMA_SCRIPTS_PUBLIC
                        The directory containing the anima scripts public root
                        (optional, the script will look for this information
                        in the ~/.anima/config.txt file by default).
```
