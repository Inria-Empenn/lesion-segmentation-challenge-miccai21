# FAQ

### What is the timeline of the challenge?

[The timeline of the challenge](https://portal.fli-iam.irisa.fr/msseg-2/challenge-timeline-and-pipeline-integration/) with the different deadlines is accessible on [the challenge website](https://portal.fli-iam.irisa.fr/msseg-2/).

### How should I submit my method?

The [submission guidelines](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/-/blob/master/SUBMISSION_GUIDELINES.md) contain all information to submit a method. 

Do not hesitate to ask any question at challenges-iam@inria.fr if anything is unclear.

### Can I have an example dockerfile or an example method?

There is an example method with a [dockerfile](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/-/blob/master/example_method/Dockerfile.cpu) in the [example_method](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/-/tree/master/example_method) of the [lesion-segmentation-challenge-miccai21](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/) repository.

### How to define the current directory?

The current directory will be set by the VIP platform when executing your method, so any working directory defined in the dockerfile will be overriden by the execution command. Thus you should not rely on a working directory defined by a `WORKDIR` statement during the execution of your method (try to avoid using `WORKDIR` if possible, although it could be used for installation purposes if necessary).

Your method will be executed with a command of the following kind:

`docker run --entrypoint=/bin/sh --rm -v /path/to/working/directory:/path/to/working/directory -w /path/to/working/directory dockerid/method-name:v1.0.0 command-line.sh`

The `-w` argument will override any `WORKDIR` statement in the dockerfile.

The path to the working directory (`/path/to/working/directory`) is automatically set by Boutiques, and we have no control over it ; so you should not rely on it.

### How to solve "file not found error"?

See answer above *"How to define the current directory?"*.

Do not forget to include the main script (entry point) of your method into your image.

Just copy your script in your image with a dockerfile statement like `COPY process.py /method/` and then put the full path to your script in the execution command in the descriptor file, like so `/method/process.py -t1 flair_time01.nii.gz -t2 flair_time02.nii.gz -o output_segmentation.nii.gz`.

One common reason is that the script of the method is in the working directory on the host, but it is not in the image.

**Here is an example of a common incorrect set up:**

Execution directory on the host: 

```
/home/username/method/
├── process.py
├── flair_time01.nii.gz
├── flair_time02.nii.gz
├── example_invocation.json
└── msseg_example_method_cpu.json
```

The container is launched from this directory with:

`bosh exec launch -s zenodo.1482743 ./example_invocation.json`      (this is the what the VIP platform will execute)

This will result in the following call:

`docker run --entrypoint=/bin/sh --rm -v /home/username/method/:/automatically/generated/to/working/directory -w /automatically/generated/path/to/working/directory dockerid/method-name:v1.0.0 command-line.sh`

Thus, the `process.py` file will be found, because it is on the execution directory. Everything looks fine when you test the method from this `/home/username/method/` directory.
But the `process.py` file will not be present in the execution directory on the VIP platform.

**Instead the process.py file must be included in the image.**

In the example method, the last statement copies the `process.py` script into the `/nnunet/`:

`COPY process.py /nnunet/`

And the command line defined in the descriptor contains the full path to the script: 

`python /nnunet/process.py -t1 [FLAIR1] -t2 [FLAIR2] -o [SEGMENTATION]`.

In this way, the script will be found no matter where the method is executed.

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

### How can I include the provided preprocessing scripts in my image?

You can easily get the anima tools required to preprocess your data in your image by copying lines 3 to 17 at the beginning of the dockerfile of your image (after the FROM statement):

```
[...] # FROM statement of your image, something like "FROM python:slim-buster"

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils ca-certificates wget unzip git git-lfs
RUN update-ca-certificates

WORKDIR /anima/

RUN wget -q https://github.com/Inria-Visages/Anima-Public/releases/download/v4.0.1/Anima-Ubuntu-4.0.1.zip
RUN unzip Anima-Ubuntu-4.0.1.zip
RUN git lfs install
RUN git clone --depth 1 https://github.com/Inria-Visages/Anima-Scripts-Public.git
RUN git clone --depth 1 https://github.com/Inria-Visages/Anima-Scripts-Data-Public.git
RUN mkdir /root/.anima/

COPY config.txt /root/.anima

RUN mkdir /data/

[...] # The rest of your dockerfile

```

You will need to copy the [`config.txt`](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/-/blob/master/preprocess/config.txt) in the directory where you build your image.

This will allow you to run the anima preprocessing script `/anima/Anima-Scripts-Public/ms_lesion_segmentation/animaMSLongitudinalPreprocessing.py` in your image (from the scripts of your method).

### How can I find some help?

Do not hesitate to ask any question at challenges-iam@inria.fr if anything is unclear.