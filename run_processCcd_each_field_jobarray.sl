#!/bin/bash -l

#SBATCH -p shared  
#SBATCH -n 4
#SBATCH --mem=8GB
#SBATCH -t 02:00:00     
#SBATCH -J wiynrun_project
#SBATCH -L project
#SBATCH -C haswell
#SBATCH --array=0-81

export OMP_NUM_THREADS=4

# module swap pgi gcc

# Set up LSST environment for WIYN+WHIC
# LSST Stack Conda installed maintained by Heather Kelly

# Twinkles Hack Weeek version
source /global/common/cori/contrib/lsst/lsstDM/setupStack-12_1.sh

# obs_lsstSim 12.1 + one commit
setup -j -r /global/homes/w/wmwv/local/lsst/obs_file
setup -j -r /global/homes/w/wmwv/local/lsst/meas_base

# Overwrite the catalog location to get the 2MASS catalogs.
export ASTROMETRY_NET_DATA_DIR=/project/projectdirs/m1727/cat/2MASS

# WIYN=${HOME}/tmp
WIYN=/global/project/projectdirs/lsst/wmwv/test/
REPO=${WIYN}/test_dr1

# Here's how we construct this in theory, but we have to already
# know it to determine things like how many jobs to request in the array.
#SNARR = `find $REPO/raw -name "*_?_*_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].lsst.fits" -exec basename {} \; | cut -f 1 -d _ | sort | uniq > field.list`
SNARR=(`cat field.list`)
snname=${SNARR[$SLURM_ARRAY_TASK_ID]}

echo "snname: $snname"

IMAGES=`find $REPO/raw -name "${snname}_?_*_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].lsst.fits" -exec basename {} \;`
# echo $IMAGES[*]

for imfile in ${IMAGES[*]}; do
    processCcd.py ${REPO} \
        -j 4 \
        --id filename=$imfile \
        --output ${REPO} \
        -C processCcd.config \
        --clobber-config \
        --clobber-version
done
