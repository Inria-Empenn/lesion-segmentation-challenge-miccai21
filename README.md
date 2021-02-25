# Preprocessing - Longitudinal Multipel Sclerosis Lesion Segmentation Challenge - MICCAI21

Data preprocessing for the Longitudinal Multipel Sclerosis Lesion Segmentation Challenge of MICCAI 2021.

The preprocessing consists in three steps:
 - brain extraction
 - bias correction
 - crop from the union of brain masks of both time points

This project uses [anima](https://anima.irisa.fr/) to preprocess the data.

## Usage

Run `preprocess.py -i /path/to/data/raw/ -o /path/to/data/preprocessed/` either with Docker or Singularity (easier) or in a python environment (not so hard anyway).

The `/path/to/data/raw/` directory corresponds to the training or the testing set of the challenge, and must follow this structure:

```
/path/to/data/raw/
├── 013
│   ├── flair_time01_on_middle_space.nii.gz
│   ├── flair_time02_on_middle_space.nii.gz
│   ├── ground_truth_expert1.nii.gz
│   ├── ground_truth_expert2.nii.gz
│   ├── ground_truth_expert3.nii.gz
│   ├── ground_truth_expert4.nii.gz
│   └── ground_truth.nii.gz
├── 015
│   ├── flair_time01_on_middle_space.nii.gz
│   ├── flair_time02_on_middle_space.nii.gz
│   ├── ground_truth_expert1.nii.gz
│   ├── ground_truth_expert2.nii.gz
│   ├── ground_truth_expert3.nii.gz
│   ├── ground_truth_expert4.nii.gz
│   └── ground_truth.nii.gz
...
```
### With Docker or Singularity

Build the image:

`docker build -t preprocess_lmslsc21:1.0  .` (with Docker)
 or
`sudo singularity build preprocess.sif preprocess.def` (with Singularity)

Run the image:

`docker run -v /path/to/data/:/data/ preprocess_lmslsc21:1.0 -i /data/raw/ -o /data/preprocessed/` (with Docker)
 or
`singularity run --bind /path/to/data/:/data/ preprocess.sif -i /data/raw/ -o /data/preprocessed/` (with Singularity)

The `-v` (Docker) or `--bind` (Singularity) option mounts a volume from the host to the container; `/path/to/data/` must be the path to the directory containing the dataset you want to preprocess (for example `/data/lmslsc21/training/`) so that it becomes available in the container.
The `preprocessed/` directory will be created (`/path/to/data/preprocessed/`) and contain the preprocessed data with the same structure as the raw data (described above).

### In a python environment

#### Installation

 1. Download the Anima Binaries [from the download page](https://anima.irisa.fr/downloads/)
 2. Clone the [Anima Scripts Public repository](https://github.com/Inria-Visages/Anima-Scripts-Public)
 3. Clone the [Anima Scripts Public Data repository](https://github.com/Inria-Visages/Anima-Scripts-Data-Public/) containing the template used for the brain extraction
 4. Create the `~/.anima/config.txt` file to configure anima (or copy it ), containing the following paths:
 

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
#### Execution


```
preprocess.py [-h] -i INPUT -o OUTPUT [-a ANIMA]
                     [-s ANIMA_SCRIPTS_PUBLIC]

Preprocess data for the Longitudinal MS Lesion Segmentation Challenge of
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