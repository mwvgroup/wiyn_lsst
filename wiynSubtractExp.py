#!/usr/bin/env python

from __future__ import division, print_function

import os

import numpy as np


def calc_fwhm_from_exp(exp):
    """Estimate FWHM from an Exposure that has a PSF"""
    # If we multiply a Gaussian sigma by the following
    # we get the Gaussian FWHM
    # For other shapes, there's no such guarantee, but it's still useful
    sigma2fwhm = 2*np.sqrt(2*np.log(2))

    fwhm = None
    if exp.hasPsf():
        quad = exp.getPsf().computeShape()
        s = quad.getDeterminantRadius()  # sigma for circular PSFs
        fwhm = s * sigma2fwhm

    return fwhm


def smoothExp(exp, fwhm, display=False):
    import lsst.afw.math as afwMath

    smoothedScienceExposure = exp.clone()
    gauss = afwMath.GaussianFunction1D(fwhm)
    kSize = int(2*fwhm + 0.5) + 1
    kernel = afwMath.SeparableKernel(kSize, kSize, gauss, gauss)
    afwMath.convolve(smoothedScienceExposure.getMaskedImage(), exp.getMaskedImage(), kernel)

    if display:
        import lsst.afw.display.ds9 as ds9
        ds9.mtv(exp, title="science", frame=1)
        ds9.mtv(smoothedScienceExposure, title="smoothed", frame=2)

    return smoothedScienceExposure


def subtractExposures(scienceExposure, templateExposure):
    import lsst.ip.diffim as ipDiffim

    # Some configuration (no clear idea of what it is)
    config = ipDiffim.ImagePsfMatchTask.ConfigClass()
    config.kernel.name = "AL"
    subconfig = config.kernel.active

    fwhmT = fwhmS = defFwhm = 7.5

    if templateExposure.hasPsf():
        fwhmT = calc_fwhm_from_exp(templateExposure)
    print('USING: FwhmT =', fwhmT)

    if scienceExposure.hasPsf():
        fwhmS = calc_fwhm_from_exp(scienceExposure)
    print('USING: FwhmS =', fwhmS)

    # Some code from RHL to try the self-convolution approach
    # In principle, the resulting difference image
    preConvolve = False
    if preConvolve:
        smoothedScienceExposure = smoothExp(scienceExposure, fwhmS)
        fwhmS *= np.sqrt(2)
        smoothedTemplateExposure = smoothExp(templateExposure, fwhmT)
        fwhmT *= np.sqrt(2)

        scienceExposure = smoothedScienceExposure
        templateExposure = smoothedTemplateExposure

    if preConvolve or fwhmS > fwhmT:
        convolveTemplate = True
    else:
        convolveTemplate = False

    psfmatch = ipDiffim.ImagePsfMatchTask(config)
    results = psfmatch.subtractExposures(templateExposure, scienceExposure,
                                         templateFwhmPix=fwhmT, scienceFwhmPix=fwhmS,
                                         convolveTemplate=convolveTemplate )

    return results

# Taken from Dominique Fouchez
# who in turn I believe took the example from ip_diffim/examples/runSubtractExposure.py
def subtractFiles(scienceFilename, templateFilename, outputFilename, outputConvFilename=None):
    import lsst.afw.image as afwImage

    from astropy.io import fits

    # Make sure directory exists
    outdir = os.path.dirname(outputFilename)
    # Sure, should check to see if it's actually a directory
    #  but I don't have any plans to do anything intelligent if
    #  the outdir exists but is not a directory, so we'll just let this fail.
    if outdir != '' and not os.path.exists(outdir):  os.makedirs(outdir)

    # Now read the images with afwImage.ExposureF
    templateExposure = afwImage.ExposureF(templateFilename)
    scienceExposure = afwImage.ExposureF( scienceFilename)

    results = subtractExposures(scienceExposure, templateExposure)

    # Finalize by writing the output file of the image difference
    results.subtractedExposure.writeFits(outputFilename)
    if outputConvFilename is not None:
        # and the convolved template image
        results.matchedImage.writeFits(outputConvFilename)


def testloop():
    (scienceFilename, templateFilename, outputFilename) = ('/global/homes/w/wmwv/workspace/iPTF13dge/iPTF13dge_A_H_20131020/iPTF13dge_A_H_20131020.lsst.fits', '/global/homes/w/wmwv/workspace/iPTF13dge/iPTF13dge_A_H_20131018/iPTF13dge_A_H_20131018.lsst.fits', '/global/homes/w/wmwv/workspace/iPTF13dge/diff/iPTF13dge_A_H_20131020_iPTF13dge_A_H_20131018.diff.fits')
    subtractFiles(scienceFilename, templateFilename, outputFilename)


def convname_from_diffname(diffname):
    """Replace everything after the first '.' with 'conv.fits'"""
    return diffname.partition('.')[0] + '.conv.fits'


def diffname_from_inputs(infile, outfile):
    """Concatenate infile, outfile to generate difffile."""
    return "{}_{}.diff.fits".format(os.path.basename(infile).partition('.')[0],
                                    os.path.basename(outfile).partition('.')[0])


############################
if __name__=="__main__":
    import os, sys

    try:
        print(sys.argv[1:4])
        (imfile, reffile, outfile) = sys.argv[1:4]
    except:
        testloop()

    convfile = convname_from_diffname(outfile)
    subtractFiles(imfile, reffile, outfile, convfile)
