# MICCAI 2021 - Longitudinal Multiple Sclerosis Lesion Segmentation Challenge 

This dataset is composed of MR neuroimaging data of 100 patients selected from the [HD Cohort](http://www.ofsep.org/en/hd-cohort) of the [French Registry on Multiple Sclerosis](http://www.ofsep.org/en/).

For each patient, 3D FLAIR images have been acquired at two time points, with varying interval of time between the two scans.
Those images were then registered in the intermediate space between the two time points. First, the transformation to go from the space of the first time point to the space of the second time point was computed. Then, half of this transformation was applied on the first time point, and half of the opposite transformation was applied on the second time point. In this way, both images have similar interpolation artifacts.

4 experts manually segmented new Multiple Sclerosis lesions (lesions appearing on the second time point, but not the first). All lesions delineated by three of four experts were selected, and another expert reviewed the remaining lesions (those delineated by two or less experts) to validate or reject them. 
A voxel wise majority voting was applied to create the final consensus masks. In other words, each lesion voxel is considered as part of a lesion if half or more of the concerned experts delineated the voxel. 
For example, if a lesion was segmented by three experts, all lesion voxels delineated by two or more experts were validated as lesion voxels ; but not the ones delineated by a single expert.
Similarly, if a lesion was segmented by two experts, all of the lesion voxels were validated as lesion voxels.

The dataset is split in one training set and one testing set, in such way that 60% of the lesions belong to the testing set.

The files follow this structure:

```
/OFSEP_GT/training/
├── 013
│   ├── flair_time01_on_middle_space.nii.gz
│   ├── flair_time02_on_middle_space.nii.gz
│   ├── ground_truth_expert1.nii.gz
│   ├── ground_truth_expert2.nii.gz
│   ├── ground_truth_expert3.nii.gz
│   ├── ground_truth_expert4.nii.gz
│   └── ground_truth.nii.gz
├── 015
│   ├── flair_time01_on_middle_space.nii.gz
│   ├── flair_time02_on_middle_space.nii.gz
│   ├── ground_truth_expert1.nii.gz
│   ├── ground_truth_expert2.nii.gz
│   ├── ground_truth_expert3.nii.gz
│   ├── ground_truth_expert4.nii.gz
│   └── ground_truth.nii.gz
├── 016
...
```

where:
 - `flair_time01_on_middle_space.nii.gz` and `flair_time02_on_middle_space.nii.gz` are the 3D FLAIR images at two time points.
 - `ground_truth_expertN.nii.gz` (where N goes from 1 to 4) are the original segmentations of each experts,
 - and `ground_truth.nii.gz` is the consensus.

Instructions to preprocess the data with anima can be found in [the dedicated repository](https://gitlab.inria.fr/amasson/lesion-segmentation-challenge-miccai21/).