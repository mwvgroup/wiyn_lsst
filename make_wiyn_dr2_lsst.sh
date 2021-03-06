source ~wmwv/.bashrc.wiyn
# export PATH=$PATH:/global/homes/w/wmwv/local/bin

setup -k -r ~wmwv/local/lsst/obs_wiyn

# Don't include .expmap.fits or previous .lsst.fits files
#  Just the image stacks themselves, which end in YYYYMMDD.fits
python wiynAssembleExp.py ${DR2BASE}/stacks/*[0-9].fits

# Sample from 2011A
# for sn in PSNJ07250042\+2347030 LSQ12fuk PTF11pbp PTF11qzq PTF11mty SN2011iu SN2011gy PTF11owc SN2011ho PTF11qpc; do
#    python wiynAssembleExp.py ${DR1BASE}/stacks/${sn}_*[0-9].fits
# done
