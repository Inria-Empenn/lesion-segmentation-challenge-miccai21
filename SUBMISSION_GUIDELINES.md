# Submit a method for the MSSeg Challenge

Methods will be evaluated on the [Virtual Imaging Platform (VIP)](https://vip.creatis.insa-lyon.fr/), which is a web portal for medical simulation and image data analysis.

To publish your method on VIP, you need to perform the following steps:

1. build a Docker or Singularity image containing your method,
1. create a [Boutiques](https://boutiques.github.io/) descriptor of your tool,
1. make your image and descriptor available to the [VIP team](mailto:vip-support@creatis.insa-lyon.fr).

Your method will then be imported on the VIP platform by VIP admins, and you will be able to test it with some example data available on the platform.

Practically, your method should process one patient at a time. It should take two FLAIR images as inputs (the time points of the patient), and output one segmentation image (a binary mask equal to 1 where there is a new MS lesion and 0 elsewere). Input and output names must be explicit in the command-line, as in the following example:

`method -t1 flair_time01.nii.gz -t2 flair_time02.nii.gz -o output_segmentation.nii.gz`

During the evaluation, your method will be executed by the VIP team on all 60 patients of the test dataset, and the output segmentations will be processed by a future version of [animaSegPerfAnalyzer](https://anima.readthedocs.io/en/latest/segmentation.html#segmentation-performance-analyzer) (modified for the need of the challenge).

## Build a Docker or Singularity image

You must provide a built image containing your method. Please refer to the [Docker](https://docs.docker.com/get-started/) or [Singularity](https://sylabs.io/guides/3.7/user-guide/quick_start.html) documentation to build your image.

Ultimately, your method will be executed on the VIP platform with an automatically generated command of the following kind:

`docker run --entrypoint=/bin/sh --rm  -v /path/to/working/directory:/path/to/working/directory -w /path/to/working/directory dockerid/method-name:latest command-line.sh`

VIP will provide the input data for your method (the two FLAIR images) in the working directory of your container.  Your method should thus look for inputs in the working directory and generate the segmentation file at the same location.

The `command-line.sh` file will also be automatically generated to call your method with one patient of the test data of the challenge ; it will contain something like `method -t1 flair_time01_025.nii.gz -t2 flair_time02_025.nii.gz -o segmentation_025.nii.gz`.

Here are the VIP guidelines for Docker images:

    - For efficient management of containers in VIP, we recommend that containers use the following images if possible:
        - Linux distribution: [centos7](https://hub.docker.com/r/_/centos/) (official).
        - Compiled Matlab applications: [viplatform/matlab-compiler-runtime](https://hub.docker.com/r/viplatform/matlab-compiler-runtime) (unofficial).
        - Applications using MRtrix3: [glatard/mrtrix3](https://hub.docker.com/r/glatard/mrtrix3/) (unofficial).
    - Compiled applications: avoid using architecture-specific compilation flags as it will produce non-portable code (Illegal instruction error messages).
    - Your application is supposed to work with a regular user (not as root).

In addition to these guidelines, please note that VIP has mainly access to 'standard' shared compute resources, with limited numbers of cores and RAM. Your method should not automatically make use of all available CPUs, but allow for the turning ON/OFF of the parallelisation (e.g., with a flag). 
Moreover, whenever possible, please provide a CPU implementation of your method since we may not have access to GPUs in due time for the integration of your application.

## Publish your image (or transfer it to VIP via sftp)

Follow [the Docker instructions](https://docs.docker.com/get-started/04_sharing_app/) or [the Singularity instructions](https://sylabs.io/guides/3.7/user-guide/endpoint.html) to publish your method somewhere accessible to the VIP platform. 

We encourage you to publish your image in a public repository, but you can also use a private one if you prefer. If you publish it in a private repository, you will have to [contact the VIP team](mailto:vip-support@creatis.insa-lyon.fr) to provide them the authentication information to download the image.

Alternatively, you can [contact the VIP team](mailto:vip-support@creatis.insa-lyon.fr) and ask to send your image via sftp.

The URL of your image will be given in the Boutiques descriptor as described bellow. The VIP platform will read this URL from the descriptor to download your image.

## Create the Boutiques descriptor

The Boutiques descriptor is a json file describing how to execute your method.

The simplest way to create it is to copy the example descriptor `example_method/msseg_example_method_cpu.json` from this repository, and replace the fields "name", "description", "author", "command-line" and "container-image" with the appropriate information.

The "command-line" field should reflect the command you use to execute your method, with the two input names `[FLAIR1]` and `[FLAIR2]` the output image `[SEGMENTATION]`, as follows:

`"command-line": "python process.py -t1 [FLAIR1] -t2 [FLAIR2] -o [SEGMENTATION]"`

As you can see in the example descriptor, the fields "value-key" of the "inputs" refer to the input names `[FLAIR1]`, `[FLAIR2]` and `[SEGMENTATION]`; please try to keep this format so that all methods follow the same scheme. Also note that the "output_segmentation" input is of type String as it serves to define the output file name.

Under the hood, the VIP platform will use Boutiques to:
- download your image from the URL in the descriptor,
- generate the command lines to execute your method.

The Boutiques descriptor provides all the information necessary to generate the command lines to exectue your method.

Thus, VIP will be able to call your method on all 60 patients of the evaluation dataset.

For more information about [Boutiques](https://boutiques.github.io/) you can follow [the Boutiques tutorial](https://nbviewer.jupyter.org/github/boutiques/tutorial/blob/master/notebooks/boutiques-tutorial.ipynb) but this is not required to participate to the challenge.

If you decide to install Boutiques, you can verify that your descriptor is valid with the following command: `bosh validate your-method-descriptor.json`.

## Send your descriptor to the VIP team

Once you have built your image and your Boutiques descriptor is ready, you can send it via email to the VIP team at [vip-support@creatis.insa-lyon.fr](mailto:vip-support@creatis.insa-lyon.fr) (just join the json file and explain that you would like to add your method to VIP for the MSSeg challenge). Once the VIP team has installed your method on the platform, you will be able to execute it on the example data for testing purposes through [the VIP interface](https://vip.creatis.insa-lyon.fr/).
You will have to carefully validate the results obtained on VIP with the testing data and report to the VIP team if you encounter any issues. 

That's it! You have successfully submitted your method to the MSSeg Challenge.
Once all methods have been evaluation on all 60 patients of the test dataset, results will be published in a dedicated publication.

## (Optional) Publish your descriptor

You can publish your descriptor on [Zenodo](https://zenodo.org/) and make your method available to others by following [the Boutiques tutorial](https://nbviewer.jupyter.org/github/boutiques/tutorial/blob/master/notebooks/boutiques-tutorial.ipynb).
Nevertheless, we advise you to validate the descriptor with the VIP team before publishing it on Zenodo. This is because we may need to modify it and Zenodo does not allow for the update of existing files. You will thus have to create a new file or a new version of the existing one. 

Alternatively, once your method is integrated in VIP, you can ask the VIP team to publish the descriptor for you if your prefer.

Of course, this step is optional and you can decide not to publish your tool at all.

Once published, the tools are easily accessible using the following Boutiques commands:

-`bosh search toolname` to search a tool from the Zenodo database (this will return a list of matching tools with their zenodoID),
-`bosh exec launch -s zenodoID example_invocation.json` to execute the tool with the arguments described in the `example_invocation.json` file.

Boutiques will automatically and transparently download and execute the image containing the tools, making them easy to use anywhere.
