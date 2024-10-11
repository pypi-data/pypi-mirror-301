#!/usr/bin/env python

import sys
import shutil
import os
import argparse
import surfa as sf
import json
import samseg 
import numpy as np
from samseg import SAMSEGDIR

def parseArguments(argv):

    # ------ Parse Command Line Arguments ------

    parser = argparse.ArgumentParser()

    default_threads = int(os.environ.get('OMP_NUM_THREADS', 1))

    # required
    parser.add_argument('-t', '--timepoint', nargs='+', action='append', required=True, help='Configure a timepoint with multiple inputs.')
    parser.add_argument('-o', '--output', required=True, help='Output directory.')
    # optional lesion options
    parser.add_argument('--lesion', action='store_true', default=False, help='Enable lesion segmentation (requires tensorflow).')
    parser.add_argument('--threshold', type=float, default=0.3, help='Lesion threshold for final segmentation. Lesion segmentation must be enabled.')
    parser.add_argument('--samples', type=int, default=50, help='Number of samples for lesion segmentation. Lesion segmentation must be enabled.')
    parser.add_argument('--burnin', type=int, default=50, help='Number of burn-in samples for lesion segmentation. Lesion segmentation must be enabled.')
    parser.add_argument('--lesion-mask-structure', default='Cortex', help='Intensity mask brain structure. Lesion segmentation must be enabled.')
    parser.add_argument('--lesion-mask-pattern', type=int, nargs='+', help='Lesion mask list (set value for each input volume): -1 below lesion mask structure mean, +1 above, 0 no mask. Lesion segmentation must be enabled.')
    parser.add_argument('--do-not-use-shape-model', action='store_true', default=False, help='Do not use the lesion shape model (VAE). Lesion segmentation must be enabled.')
    # optional processing options
    parser.add_argument('-m', '--mode', nargs='+', help='Output basenames for the input image mode.')
    parser.add_argument('-a', '--atlas', metavar='DIR', help='Point to an alternative atlas directory.')
    parser.add_argument('--init-reg', metavar='FILE', help='Initial affine registration.')
    parser.add_argument('--deformation-hyperprior', type=float, default=20.0, help='Strength of the latent deformation hyperprior.')
    parser.add_argument('--gmm-hyperprior', type=float, default=0.5, help='Strength of the latent GMM hyperprior.')
    parser.add_argument('--options', metavar='FILE', help='Override advanced options via a json file.')
    parser.add_argument('--pallidum-separate', action='store_true', default=False, help='Move pallidum outside of global white matter class. Use this flag when T2/flair is used.')
    parser.add_argument('--threads', type=int, default=default_threads, help='Number of threads to use. Defaults to current OMP_NUM_THREADS or 1.')
    parser.add_argument('--tp-to-base-transform', nargs='+', required=False, help='Transformation file for each time point to base.')
    parser.add_argument('--force-different-resolutions', action='store_true', default=False, help='Force run even if time points have different resolutions.')
    # optional debugging options
    parser.add_argument('--history', action='store_true', default=False, help='Save history.')
    parser.add_argument('--save-posteriors', nargs='*', help='Save posterior volumes to the "posteriors" subdirectory.')
    parser.add_argument('--save-probabilities', action='store_true', help='Save final modal class probabilities to "probabilities" subdirectory.')
    parser.add_argument('--showfigs', action='store_true', default=False, help='Show figures during run.')
    parser.add_argument('--save-warp', action='store_true', help='Save the image->template warp fields.')
    parser.add_argument('--save-mesh', action='store_true', help='Save the final mesh of each timepoint in template space.')
    parser.add_argument('--movie', action='store_true', default=False, help='Show history as arrow key controlled time sequence.')

    args = parser.parse_args(argv)

    return args

# ------ Initial Setup ------

def main():

    args = parseArguments(sys.argv[1:])

    # Make sure more than 1 timepoint was specified
    if len(args.timepoint) == 1:
        sf.system.fatal('must provide more than 1 timepoint')

    # Make sure that the resolution of each time point is below MAXRESDIFF
    MAXRESDIFF = 0.05
    # Load each time point and check their resolution differences
    voxel_sizes = np.zeros([len(args.timepoint), 3])
    for t, timepoint in enumerate(args.timepoint):
        voxel_sizes[t, :] = sf.load_volume(timepoint[0]).geom.voxsize
    if np.min(np.diff(voxel_sizes, axis=0)) > MAXRESDIFF and not args.force_different_resolutions:
        sf.system.fatal('Time points have resolution differences greater than %s. If you want to continue, include the flag --force-different-resolutions in your command' %str(MAXRESDIFF))

    # Create the output folder
    os.makedirs(args.output, exist_ok=True)

    # Specify the maximum number of threads the GEMS code will use
    samseg.gems.setGlobalDefaultNumberOfThreads(args.threads)

    # Get the atlas directory
    if args.atlas:
        atlasDir = args.atlas
    else:
        # Atlas defaults
        if args.lesion:
            from samseg.SamsegUtility import createLesionAtlas
            # Create lesion atlas on the fly, use output directory as temporary folder
            os.makedirs(os.path.join(args.output, 'lesion_atlas'), exist_ok=True)
            atlasDir = os.path.join(args.output, 'lesion_atlas')
            createLesionAtlas(os.path.join(SAMSEGDIR, 'atlas', '20Subjects_smoothing2_down2_smoothingForAffine2'),
                              os.path.join(SAMSEGDIR, 'atlas', 'Lesion_Components'),
                              atlasDir)
        else:
            atlasDir = os.path.join(SAMSEGDIR, 'atlas', '20Subjects_smoothing2_down2_smoothingForAffine2')


    # Setup the visualization tool
    visualizer = samseg.initVisualizer(args.showfigs, args.movie)

    # Load user options from a JSON file
    userModelSpecifications = {}
    userOptimizationOptions = {}
    if args.options: 
        with open(args.options) as f:
            userOptions = json.load(f)
        if userOptions.get('modelSpecifications') is not None:
            userModelSpecifications = userOptions.get('modelSpecifications')
        if userOptions.get('optimizationOptions') is not None:
            userOptimizationOptions = userOptions.get('optimizationOptions')

    # Start the process timer
    timer = samseg.Timer()

    # Check if --save-posteriors was specified without any structure search string
    if args.save_posteriors is not None and len(args.save_posteriors) == 0:
        savePosteriors = True
    else:
        savePosteriors = args.save_posteriors

    # define LTA type - reused from transform.h
    type_descriptions = {
        0: "LINEAR_VOX_TO_VOX",
        1: "LINEAR_RAS_TO_RAS",
        2: "LINEAR_PHYSVOX_TO_PHYSVOX",
        10: "TRANSFORM_ARRAY_TYPE",
        11: "MORPH_3D_TYPE",
        12: "MNI_TRANSFORM_TYPE",
        13: "MATLAB_ASCII_TYPE",
        14: "REGISTER_DAT",
        15: "FSLREG_TYPE",
        21: "LINEAR_CORONAL_RAS_TO_CORONAL_RAS",
        "LINEAR_VOX_TO_VOX": "LINEAR_VOXEL_TO_VOXEL",
        "LINEAR_CORONAL_RAS_TO_CORONAL_RAS": "LINEAR_COR_TO_COR",
    }

    def check_lta_file(filepath):
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    if "type" in line.lower():
                        # Extract the type value, accounting for variable spacing around '='
                        type_value = line.split('=')[-1].strip()
                        try:
                            type_value = int(type_value)
                        except ValueError:
                            pass  # Keep as string if conversion fails, to handle descriptive keys
                        
                        if type_value == 1:
                            return True, "LTA is of type RAS-to-RAS, proceeding as before."
                        elif type_value in type_descriptions:
                            error_message = f"Error: LTA file type is {type_descriptions[type_value]}. Convert to RAS-to-RAS and try again."
                            return False, error_message
                        else:
                            return False, "Error: LTA file type is of an unknown type."
            return False, "Error: 'Type' line not found in the file - unable to determine if LTA is of type RAS-to-RAS."
        except Exception as e:
            return False, f"An error occurred: {str(e)}"
    
    tpToBaseTransforms = []
    if args.tp_to_base_transform:
        for tpTobase in args.tp_to_base_transform:
            should_continue, message = check_lta_file(tpTobase)
            if should_continue:
                tpToBaseTransforms.append(sf.load_affine(tpTobase))
            else:
                print(message)
                sys.exit(1)
    else:
        print("Assuming an identity transformation between base and each time point")
        for tp in args.timepoint:
            tpToBaseTransforms.append(sf.Affine(np.eye(4)))


    # ------ Run Samsegment ------

    samseg_kwargs = dict(
        imageFileNamesList=args.timepoint,
        atlasDir=atlasDir,
        savePath=args.output,
        userModelSpecifications=userModelSpecifications,
        userOptimizationOptions=userOptimizationOptions,
        targetIntensity=110,
        targetSearchStrings=['Cerebral-White-Matter'],
        modeNames=args.mode,
        pallidumAsWM=(not args.pallidum_separate),
        saveModelProbabilities=args.save_probabilities,
        strengthOfLatentDeformationHyperprior=args.deformation_hyperprior,
        strengthOfLatentGMMHyperprior=args.gmm_hyperprior,
        savePosteriors=savePosteriors,
        saveMesh=args.save_mesh,
        saveHistory=args.history,
        visualizer=visualizer,
        tpToBaseTransforms=tpToBaseTransforms,
    )

    if args.lesion:

        # If lesion mask pattern is not specified, assume inputs are T1-contrast
        lesion_mask_pattern = args.lesion_mask_pattern
        if lesion_mask_pattern is None:
            lesion_mask_pattern = [0] * len(args.timepoint[0])
            print('Defaulting lesion mask pattern to %s' % str(lesion_mask_pattern))

        # Delay import until here so that tensorflow doesn't get loaded unless needed
        from samseg.SamsegLongitudinalLesion import SamsegLongitudinalLesion
        samsegLongitudinal = SamsegLongitudinalLesion(**samseg_kwargs,
            intensityMaskingSearchString=args.lesion_mask_structure,
            intensityMaskingPattern=lesion_mask_pattern,
            numberOfBurnInSteps=args.burnin,
            numberOfSamplingSteps=args.samples,
            threshold=args.threshold,
            sampler=not args.do_not_use_shape_model
        )

    else:
        samsegLongitudinal = samseg.SamsegLongitudinal(**samseg_kwargs)

    samsegLongitudinal.segment(saveWarp=args.save_warp, initTransformFile=args.init_reg)

    timer.mark('run_samseg_long complete')

    # If lesion atlas was created on the fly, remove it
    if not args.atlas and args.lesion:
        shutil.rmtree(os.path.join(args.output, 'lesion_atlas'))

if __name__ == '__main__':
    main()
