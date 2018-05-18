Processing of SweetSpot WIYN images using LSST DM Stack.

Requires the definition of the environment variable DR1BASE and the existence of SweetSpot stacks in ${DR1BASE}/stacks.

### Run the following to process
1. Create LSST-formatted FITS with image, weight map, and mask.
`sh make_wiyn_dr1_lsst.sh`
2. Ingest files
`sh ingest_wiyn_dr1_images.sh`
3. processCcd files
`sh run_processCcd.sh`
4. coadd files
`sh run_make_all_skymaps.sh
`sh run_all_coadds.sh`
5. Photometry coadds
`sh run_all_photometry.sh`
6. Run lightcurves on calexps based on coadd detections
`. run_all_calexp_lightcurves.sh`
`. run_2mass_all_star_lightcurves.sh`

7. Run subtractions
`python sub_wiyn_dr1.py`
8. Run lightcurves on subtractions
`python wiyn_forcedPhotExternalCatalog.py`

Notes:
1. Generate "dr1_dataid.list" after ingest step with
 * sqlite3 registry.sqlite3
.separator ','
.output dr1_dataid.csv
select field, seq, filter, night, expnum from stack;
 Then reprocess with
cat dr1_dataid.csv | awk -F , '{printf "--id field=%s seq=%s filter=%s night=%s\n", $1, $2, $3, $4}' > dr1_dataid.list
2. Generate "dr1_coadd.list" using
cat dr1_dataid.csv | awk -F , '{print $2, $4, $3, $1}' | grep ' H '  | sort -k 4 | uniq -f 3 | awk '{print $4, NR-1, $1, $2}' > dr1_coadd.list
3. Generate "dr1_coadd.list" for images actually successfully processed to calexp stage:
ls ${REPO}/rerun/processCcd/calexp/bkgd*| cut -d / -f 11 | sed -e 's/bkgd-\(.*\)_\([A-F]\)_\([JHKS]*\)_\([0-9]\{8\}\)_\([0-9][0-9]*\)\.fits/\2 \3 \4 \5 \1/' | sort -k 5 | uniq -f 4 | awk '{print $5, NR-1, $1, $2, $3}' > dr1_coadd_actual.list

### Batch queue processing (SLURM)
The simplest job would just be to run the above commands in a single-node, serial job.

The slightly more efficient job spreads out the processing of the processCcd step, which is the the most expensive step.

3. processCcd
`sbatch run_processCcd_each_field_jobarray.sl`
4. Run subtractions
`sbatch run_subtractions.sl`
5. Run lightcurves
`sbatch run_forced_photometry.sl`
Want to run LSST DM Stack on NERSC. The install from Twinkles is here:

https://github.com/mwvgroup/wiyn_lsst.git

The git issue discussing this install is https://github.com/DarkEnergyScienceCollaboration/Twinkles/issues/242.
