source ~/.bashrc.lsst

#    --id filename='PS1-12bwh_A_J_20121028.lsst.fits' \
WIYN=${HOME}/tmp
REPO=${WIYN}/test_dr1

# for fullfile in PS1-12bwh_A_J_20121028.lsst.fits PS1-12bwh_A_J_20121130.lsst.fits; do
# for fullfile in PS1-12bwh_A_J_20121028.lsst.fits; do
#for fullfile in `ls ${REPO}/raw/LSQ12fuk*`; do
#for sn in PSNJ07250042\+2347030 LSQ12fuk PTF11pbp PTF11qzq PTF11mty SN2011iu SN2011gy PTF11owc SN2011ho PTF11qpc PS1-12bwh; do
# for sn in PS1-12bwh; do
# for sn in SN2011gy; do
# for sn in SN2011gy PSNJ07250042\+2347030 LSQ12fuk PTF11pbp PTF11qzq PTF11mty SN2011iu PTF11owc SN2011ho PTF11qpc PS1-12bwh; do
#    for fullfile in `\ls ${REPO}/raw/${sn}*`; do
for fullfile in `ls ${REPO}/raw`; do
    sn_file=`basename ${fullfile}`

    processCcd.py ${REPO} \
        --id filename=${sn_file} \
        --output ${REPO} \
        -C run_wiyn.config \
        --clobber-config \
        --clobber-version 
#        --logdest ${sn_file}_processCcd.log
    #        isr.noise=100 isr.addNoise=True \
    #    --debug \
    #        calibrate.detection.thresholdType='pixel_stdev' \
    #        charImage.measurement.plugins['base_Jacobian'].pixelScale=0.1

done
# done
