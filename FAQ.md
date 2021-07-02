# FAQ

### What is the timeline of the challenge?

[The timeline of the challenge](https://portal.fli-iam.irisa.fr/msseg-2/challenge-timeline-and-pipeline-integration/) with the different deadlines is accessible on [the challenge website](https://portal.fli-iam.irisa.fr/msseg-2/).

### How should I submit my method?

The [submission guidelines](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/-/blob/master/SUBMISSION_GUIDELINES.md) contain all information to submit a method. 

Do not hesitate to ask any question at challenges-iam-request@inria.fr if anything is unclear.

### Can I have an example dockerfile or an example method?

There is an example method with a [dockerfile](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/-/blob/master/example_method/Dockerfile.cpu) in the [example_method](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/-/tree/master/example_method) of the [lesion-segmentation-challenge-miccai21](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/) repository.

### How to define the current directory?

The current directory will be set by the VIP platform when executing your method, so any working directory defined in the dockerfile will be overriden by the execution command. Thus we advise not to rely on a working directory.

Your method will be executed with a command of the following kind:

`docker run --entrypoint=/bin/sh --rm -v /path/to/working/directory:/path/to/working/directory -w /path/to/working/directory dockerid/method-name:v1.0.0 command-line.sh`

The `-w` argument will override any `WORKDIR` statement in the dockerfile.

### Where should I read the input images in my container?

Your method will read the two flair images from the input arguments, and write the segmentation defined by the output argument, as in this python example:

```
    [...]

    parser = argparse.ArgumentParser(description="Detect new MS lesions from two FLAIR images.")

    parser.add_argument('-t1', '--time01', type=str, help="First time step (path to the FLAIR image).", required=True)
    parser.add_argument('-t2', '--time02', type=str, help="Second time step (path to the FLAIR image).", required=True)
    parser.add_argument('-o', '--output', type=str, help="Path of the output segmentation.", required=True)

    args = parser.parse_args()

    flair_time01 = Path(args.time01)
    flair_time02 = Path(args.time02)
    output = Path(args.output)

    flair_time01_image = sitk.ReadImage(str(flair_time01))

    flair_time02_image = sitk.ReadImage(str(flair_time02))

    [...]

    sitk.WriteImage(segmentation, str(output))

```

Your script will be called as in the following example:

`python process.py -t1 flair_time01.nii.gz -t2 flair_time02.nii.gz -o output_segmentation.nii.gz`

You should not need worry about the path to the images, VIP will make them accessible to your method.

### How can I find some help?

Do not hesitate to ask any question at challenges-iam-request@inria.fr if anything is unclear.