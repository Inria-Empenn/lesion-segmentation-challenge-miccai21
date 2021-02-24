import sys
import os
import configparser as ConfParser
import argparse
import subprocess
import shutil
from pathlib import Path
Path.ls = lambda x: list(x.iterdir())

# Argument parsing
parser = argparse.ArgumentParser(
    description="""Preprocess data for the Longitudinal MS Lesion Segmentation Challenge of MICCAI 2021 with the anima library. 
                    The preprocessing consists in a brain extraction followed by a bias field correction.""")

parser.add_argument('-i', '--input', type=str, required=True, help='Input folder containing the patients to preprocess (for example segmentation_challenge_miccai21/training/).')
parser.add_argument('-o', '--output', type=str, required=True, help='Output folder where the processed data will be saved (it will follow the same file structure as the input folder).')
parser.add_argument('-a', '--anima', type=str, help='The directory containing the anima binaries (optional, the script will look for this information in the ~/.anima/config.txt file by default).')
parser.add_argument('-s', '--anima_scripts_public', type=str, help='The directory containing the anima scripts public root (optional, the script will look for this information in the ~/.anima/config.txt file by default).')

args = parser.parse_args()

patients = Path(args.input)
output = Path(args.output)

# The configuration file for anima is ~/.anima/config.txt (can be overridden with -a and -s arguments)
configFilePath = Path.home() / '.anima' / 'config.txt'

# Open the configuration parser and exit if anima configuration cannot be loaded
configParser = ConfParser.RawConfigParser()

if configFilePath.exists():
    configParser.read(configFilePath)
elif (not args.anima) or (not args.anima_scripts_public):
    sys.exit('Please create a configuration file (~/.anima/config.txt) for Anima python scripts.')

# Initialize anima directories
animaDir = Path(configParser.get("anima-scripts", 'anima')) if configFilePath.exists() else Path(args.anima)
animaScriptsPublicDir = Path(configParser.get("anima-scripts", 'anima-scripts-public-root')) if configFilePath.exists() else Path(args.anima_script_public)

# Anima commands
animaBrainExtraction = animaScriptsPublicDir / "brain_extraction" / "animaAtlasBasedBrainExtraction.py"
animaN4BiasCorrection = animaDir / "animaN4BiasCorrection"
animaCropImage = animaDir / "animaCropImage"
animaImageArithmetic = animaDir / "animaImageArithmetic"

# Calls a command, if there are errors: outputs them and exit
def call(command):
    command = [str(arg) for arg in command]
    status = subprocess.call(command)
    if status != 0:
        print(' '.join(command) + '\n')
        sys.exit('Command exited with status: ' + str(status))
    return status

# Preprocess all patients: 
#  - brain extraction
#  - bias correction
#  - crop
for patient in patients.ls():

    if not patient.is_dir(): continue

    print("Preprocessing patient " + patient.name + "...")

    # Create the output directory which will contain the preprocessed files
    patientOutput = output / patient.name
    patientOutput.mkdir(exist_ok=True, parents=True)
    
    masks = []

    # For both time points: extract brain and remove bias
    for flairName in ['flair_time01_on_middle_space.nii.gz', 'flair_time02_on_middle_space.nii.gz']:
        
        flair = patient / flairName
        brain = patientOutput / flairName
        mask = patientOutput / flairName.replace('.nii.gz', '_mask.nii.gz')

        # Extract brain
        call(["python", animaBrainExtraction, "-i", flair, "-S", "--mask", mask, "--brain", brain])
        # Remove bias
        call([animaN4BiasCorrection, "-i", brain, "-o", brain, "-B", "0.3"])
        
        masks.append(mask)
    
    mask = patientOutput / 'mask.nii.gz'

    # Compute the union of the masks of both time points
    call([animaImageArithmetic, "-i", masks[0], "-a", masks[1], "-o", mask])

    # Copy the ground truths to the output directory
    for imageName in ['ground_truth_expert1.nii.gz', 'ground_truth_expert2.nii.gz', 'ground_truth_expert3.nii.gz', 'ground_truth_expert4.nii.gz', 'ground_truth.nii.gz']:
        shutil.copyfile(patient / imageName, patientOutput / imageName)

    # Crop all output images with the computed mask
    for image in patientOutput.ls():
        call([animaCropImage, "-i", image, "-m", mask, "-o", image])

