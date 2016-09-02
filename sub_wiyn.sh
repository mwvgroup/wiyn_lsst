# stackDir=${DR1BASE}/'stacks'
stackDir=${HOME}/tmp/test_dr1/calexp

scienceImage='PS1-12bwh_A_J_20121028.fits'
templateImage='PS1-12bwh_A_J_20121130.fits'
outImage='PS1-12bwh_A_J_20121028_20121130.diff.fits'

scienceImage=${stackDir}/${scienceImage}
templateImage=${stackDir}/${templateImage}

# python ${IP_DIFFIM_DIR}/examples/runSubtractExposures.py ${scienceImage} ${templateImage} ${outImage}
python wiynSubtractExp.py ${scienceImage} ${templateImage} ${outImage}
