from __future__ import division

def makeLsstNamesAndFile(imfile, **kwargs):
    """Wrapper around makeLsstFile.  Formats names of expmap and output files."""
    imbase = imfile.strip(".fits")
    expfile = "{}.expmap.fits".format(imbase)
    lsstfile = "{}.lsst.fits".format(imbase)
    makeLsstFile(imfile, expfile, lsstfile, **kwargs)


def makeLsstFile(imfile, expfile, lsstfile, interpolateNans=False):
    import lsst.afw.image as afwImage
    from astropy.io import fits
    import numpy as np
    from lsst.ip.isr.isrFunctions import saturationCorrection

    gain=3.4 # WIYN WHIRC Data Reduction Guide

    imdir, imbasename = os.path.dirname(imfile), os.path.basename(imfile)
    tmp_imfile = os.path.join(imdir, "tmp_"+imbasename)
    os.system("cp {} {}".format(imfile, tmp_imfile))
#    os.system("sethead EXPID=0 {}".format(tmp_imfile))
    with fits.open(tmp_imfile, mode='update') as hdu:
	    hdu[0].header['EXPID'] = 0
	    hdu.flush()
    #Exposures should keep your header keys
    exp  = afwImage.ExposureF(tmp_imfile)
    im   = exp.getMaskedImage().getImage()
    imArr   = im.getArray()
    var  = exp.getMaskedImage().getVariance()
    varArr  = var.getArray()
    mask = exp.getMaskedImage().getMask()
    maskArr = mask.getArray()

    os.system("rm {}".format(tmp_imfile))
    # Calculate the variance based on the background level / second
    # stored in the coadd, which is the background level of
    # the first individual images included in the coadd
    # The coadd was created as an average 
    #   so is noramlized to the count level of one input image.
    expTimeArr = afwImage.ImageF(expfile).getArray()
    exphead = fits.getheader(expfile)
    exptime_per_image = exphead["EXPTIME"] # EXPTIME is not in the afwImage info (why not?) so we fall back on astropy.io.fits
    background_per_image = exphead["BGLEVEL"]
    # print "BGLEVEL: ", background_per_image
    # print "EXPTIME: ", exptime

    background_per_second = background_per_image/exptime_per_image

    fullexptime = np.percentile(expTimeArr,99)
    print (background_per_second, fullexptime, exptime_per_image)
    idx=range(int(0.2*len(maskArr[0,:])),int(0.8*len(maskArr[0,:])))

    photonArr = gain * \
      (imArr+background_per_image) * (expTimeArr/exptime_per_image) 
    ## Variance in ADU for the accumulated counts
    ##  (i.e., that has not been re-scaled to have the same normalization across the image)
    varArr[:,:] = photonArr / gain**2  
    ## Variance in ADU for the normalized image
    varArr /= (expTimeArr/exptime_per_image)**2
    varArr[np.logical_not(np.isfinite(imArr))] = np.inf 

    # Reject all of the locations with less than 20% of the effective exposure time
    idxs = np.where(expTimeArr < 0.2* fullexptime)
    badmask = mask.getPlaneBitMask('BAD')
    maskArr[idxs] |= badmask
    intrpmask = mask.getPlaneBitMask('INTRP')
    maskArr[idxs] |= intrpmask

    if interpolateNans:
        SAT_LEVEL=100000
        imArr[np.logical_not(np.isfinite(imArr))] = 2*SAT_LEVEL
        saturationCorrection(exp.getMaskedImage(), saturation=SAT_LEVEL, fwhm=2, growFootprints=False)
#    import lsst.afw.display.ds9 as ds9
#    ds9.mtv(exp, title="Foo")

    # If set, then boost the variance of low-exposure regions to 10x higher.
    # This is a bit of a hack that I'm unhappy about, but there's no
    # way to tell the current (2015-03-19) DM stack software to ignore a region.
    boostBadPixelVariance=False
    if boostBadPixelVariance:
        varArr[idxs] *= 10

    exp.writeFits(lsstfile)

def imexpfilenames(imbasename):
    # The exposure maps are not also provide in 07.wcs_calib
    expbasename=imbasename.replace("07.wcs_calib","06.stack")
    imfile="{}.fits".format(imbasename)
    expfile="{}.expmap.fits".format(expbasename)
    lsstfile="{}.lsst.fits".format(imbasename)
    return(imfile,expfile,lsstfile)

def testloop():
    date="20131025"
    sn="iPTF13dge"
    field="A"
    for f in ["J","H","KS"]:
        # imbasename="20131025/06.stack/iPTF13dge___H_OPEN"
        imbasename=os.path.join(date,"07.wcs_calib","{}_{}___{}_OPEN".format(sn,field,f))
        (imagefile,expmapfile,lsstfile)=imexpfilenames(imbasename)
        makeLsstFile(imagefile,expmapfile,lsstfile)

############################
if __name__=="__main__":
    import os, sys

    interpolateNans=True
    files = sys.argv[1:]
    for f in files:
        makeLsstNamesAndFile(f, interpolateNans=interpolateNans)
 
