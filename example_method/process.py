from subprocess import call
from pathlib import Path
import argparse
import shutil
import sys
import os

parser = argparse.ArgumentParser(description="Detect new MS lesions from two FLAIR images.")

parser.add_argument('-t1', '--time01', type=str, help="First time step (path to the FLAIR image).", required=True)
parser.add_argument('-t2', '--time02', type=str, help="Second time step (path to the FLAIR image).", required=True)
parser.add_argument('-o', '--output', type=str, help="Path of the output segmentation.", required=True)
parser.add_argument('-d', '--data_folder', type=str, help="Path of the data folder.", default='/nnunet/data/')

args = parser.parse_args()

flair_time01 = Path(args.time01)
flair_time02 = Path(args.time02)
output = Path(args.output)
data_folder = Path(args.data_folder)

# Create nnUNet directory stucture
#  input files must follow the following naming convention: case_identifier_XXXX.nii.gz
#  see [nnUNet documentation](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_conversion.md)

input_folder = data_folder / 'input' / 'nnUNet_raw_data'
input_folder.mkdir(exist_ok=True, parents=True)
input_file = input_folder / flair_time01.name.replace('.nii.gz', '_0000.nii.gz')
shutil.copy(flair_time01, input_file)

output_folder = Path.cwd() / 'output'
output_folder.mkdir(exist_ok=True)

call(['nnUNet_predict', '-i', str(input_folder), '-o', str(output_folder), '-t', '100', '-m', '3d_fullres', '-tr', 'nnUNetTrainerV2', '-f', '0'])

output_nnunet = output_folder / flair_time01.name

output_nnunet.rename(Path.cwd() / output)
