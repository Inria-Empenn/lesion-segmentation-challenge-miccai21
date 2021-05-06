# Preprocessing - Longitudinal Multipel Sclerosis Lesion Segmentation Challenge - MICCAI21

Data preprocessing for the Longitudinal Multipel Sclerosis Lesion Segmentation Challenge of MICCAI 2021.

The preprocessing consists in three or four steps:
 - brain extraction
 - bias correction
 - (optional) normalization with the given template
 - mask flair images with the union of the masks of both time points

The script is part of [Anima-Scripts-Public](https://github.com/Inria-Visages/Anima-Scripts-Public), it can be found here: `Anima-Scripts-Public/ms_lesion_segmentation/animaMSLongitudinalPreprocessing.py`.

## Usage

Run `python animaMSLongitudinalPreprocessing.py -i /path/to/data/raw/ -o /path/to/data/preprocessed/` either with Docker, Singularity or Python (see instructions bellow).

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

The output directory (`-o` option, for example `/path/to/data/preprocessed/`) will be created and contain the preprocessed data with the same structure as the raw data (described above).

You can optionally provide a template to normalize intensities with the `--template` option (must be a path to the template file, for example `path/to/template.nii.gz`).

### With Docker or Singularity

Make sure your working directory contains the `Dockerfile` or `preprocess.def` definition file; for example: `cd Longitudinal\ Multiple\ Sclerosis\ Lesion\ Segmentation\ Challenge\ Miccai21`

Build the image:

`docker build -t preprocess_lmslsc21:1.0  .` (with Docker)
 or
`sudo singularity build preprocess.sif preprocess.def` (with Singularity)

Run the image:

`docker run -v /path/to/data/:/data/ preprocess_lmslsc21:1.0 -i /data/raw/ -o /data/preprocessed/` (with Docker)
 or
`singularity run --bind /path/to/data/:/data/ preprocess.sif -i /data/raw/ -o /data/preprocessed/` (with Singularity)

The `-v` (Docker) or `--bind` (Singularity) option mounts a volume from the host into the container; `/path/to/data/` must be the path to the directory containing the dataset you want to preprocess (for example `./training/`) so that it becomes available in the container.

**Note:** you must have read and write access to the data directory in order to mount it.

If you want to normalize intensities, the template image must be accessible from the container. You can simply mount another volume containing the template file:

`docker run -v /path/to/data/:/data/ -v /path/to/template/:/template/ preprocess_lmslsc21:1.0 -i /data/raw/ -t /template/template.nii.gz -o /data/preprocessed/` (with Docker)
 or
`singularity run --bind /path/to/data/:/data/ --bind /path/to/template/:/template/ preprocess.sif -i /data/raw/ -t /template/template.nii.gz -o /data/preprocessed/` (with Singularity)

where `/path/to/template/` contains the `template.nii.gz` you want to use for the normalization.

### With python

#### Installation

*Requirement:* You need [Git LFS](https://git-lfs.github.com/) to clone the *Anima Scripts Public Data* repository with the real data (otherwise the large files will be replaced by tiny pointer files). So install Git LFS if you have not already, and run `git lfs install` before cloning anima repositories. Then, larges files from the repositories will be properly downloaded.

 1. Download the Anima Binaries [from the download page](https://anima.irisa.fr/downloads/)
 2. Clone the [Anima Scripts Public repository](https://github.com/Inria-Visages/Anima-Scripts-Public)
 3. Clone the [Anima Scripts Public Data repository](https://github.com/Inria-Visages/Anima-Scripts-Data-Public/) containing the template used for the brain extraction
 4. Create the `~/.anima/config.txt` file to configure anima (or copy it from this directory), containing the following paths:
 

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
usage: animaLongitudinalPreprocessing.py [-h] -i INPUT -o OUTPUT [-t TEMPLATE]

Preprocess data for the Longitudinal MS Lesion Segmentation Challenge of MICCAI 2021 with the anima library. 
                    The preprocessing consists in a brain extraction followed by a bias field correction.
  
  -i INPUT, --input INPUT
                        Input folder containing the patients to preprocess (for example segmentation_challenge_miccai21/training/).
                        The folder must follow this structure:
                        
                        /input/folder/
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
  -o OUTPUT, --output OUTPUT
                        Output folder where the processed data will be saved (it will follow the same file structure as the input folder).

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Path to the template image used to normalize intensities (optional, skip normalization if not given).
```

For example:

`python ~/Anima-Scripts-Public/ms_lesion_segmentation/animaLongitudinalPreprocessing.py -i ./training/ -t /path/to/template.nii.gz -o ./preprocessed/`

docker run -v /home/amasson/data/:/data/ -v /home/amasson/Anima-Scripts-Data-Public/ms-study-atlas/FLAIR/:/template/ preprocess_lmslsc21:1.0 -i /data/raw/ -t /template/FLAIR_1.nrrd -o /data/preprocessed/