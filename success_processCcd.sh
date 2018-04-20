file=processCcd.log

failures=${file}.failures

successful=`grep Photometric ${file} | wc -l`
grep FATAL ${file} > ${failures}
failed=`wc -l ${failures}`

failed_aperture_corr=`grep "Unable to measure aperture correction" ${failures} | wc -l`
failed_photocal=`grep "No matches to use for photocal" ${failures} | wc -l`
failed_no_viable_psf=`grep "No viable PSF candidates" ${failures} | wc -l`
failed_no_psf_candidates=`grep "No objects passed our cuts for consideration as psf stars" ${failures} | wc -l`
failed_too_many_cr=`grep "LengthError" ${failures} | wc -l`

failed_unknown=`cat ${failures} | grep -v  "Unable to measure aperture correction" | grep -v  "No matches to use for photocal" | grep -v  "No viable PSF candidates" | grep -v  "No objects passed our cuts for consideration as psf stars" | grep -v "LengthError"`

echo "Succeeded:  " $successful
echo "Failed   :  " $failed
echo "----"
echo "  Aperture Correction:           " $failed_aperture_corr
echo "  Photometric no matches:        " $failed_photocal
echo "  No viable PSF candidates:      " $failed_no_viable_psf
echo "  No passed PSF candidates:      " $failed_no_psf_candidates
echo "  Too many CRs:                  " $failed_too_many_cr

echo "Unknown failures: "
echo ${failed_unknown}



