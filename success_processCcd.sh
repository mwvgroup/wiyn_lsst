file=processCcd.log

successful=`grep Photometric ${file} | wc -l`
failed=`grep dataId ${file} | wc -l`

failed_aperture_corr=`grep dataId ${file} | grep "Unable to measure aperture correction" | wc -l`
failed_photocal=`grep dataId ${file} | grep "No matches to use for photocal" | wc -l`
failed_no_viable_psf=`grep dataId ${file} | grep "No viable PSF candidates" | wc -l`
failed_no_psf_candidates=`grep dataId ${file} | grep "No objects passed our cuts for consideration as psf stars" | wc -l`

echo "Succeeded:  " $successful
echo "Failed   :  " $failed
echo "----"
echo "  Aperture Correction:    " $failed_aperture_corr
echo "  Photometric no matches: " $failed_photocal
echo "  No viable PSF candidates:      " $failed_no_viable_psf
echo "  No passed PSF candidates:      " $failed_no_psf_candidates
