import os
import sys

import matplotlib.pyplot as plt
import numpy as np

from astropy.coordinates import SkyCoord
from astropy.table import Table
import astropy.units as u

import lsst.afw.display as afwDisplay
import lsst.afw.geom as afwGeom
from lsst.daf.persistence import Butler

from deepcoadd_afw_to_astropy import read_cats

from wiyn_forcedPhotExternalCatalog import assemble_catalogs_into_lightcurve


def get_field_tract_dict(file='dr1_field_tract.list'):
    data = Table.read(file, names=('field', 'tract'), format='ascii')

    field_tract_dict = {}
    for row in data:
        field_tract_dict[row['field']] = row['tract']
    return field_tract_dict


def get_tract_for_field(field):
    field_tract_dict = get_field_tract_dict()
    return field_tract_dict[field]


def get_RA_Dec_for_field(field, field_info_file='observed_target_info.dr1.txt'):
    """Return RA, Dec in decimal degrees."""
    target_info = Table.read(field_info_file, format='ascii.commented_header')

    w, = np.where(target_info['Name'] == field)
    field_info = target_info[w]
 
    # Want scalars rather than 1-element lists
    ra, dec = field_info['RA'][0], field_info['Dec'][0]
    coord = SkyCoord(ra, dec, unit=(u.hour, u.deg))

    return coord.ra.to(u.deg).value, coord.dec.to(u.deg).value


def get_dataIds_for_field(butler, field, tract=None, seq='A', patch='0,0',
                          datasetType='forced_src'):
    """Lookup available forced source in Butler."""
    if tract is None:
        tract = get_tract_from_field(field)

    # 2018-04-10:  MWV: This presently doesn't pull the correct expnums for each.
    searchDataId = {'field': field, 'seq': seq, 'tract': tract, 'patch': patch}
    cat_dataRefs = butler.subset(datasetType='forced_src', dataId=searchDataId)
    cat_dataIds = [cd.dataId for cd in cat_dataRefs]
    filters = [dId['filter'] for dId in cat_dataIds]
    uniq_filters = set(filters)
    dataIds_by_filter = {}
    for f in uniq_filters:
        these_dataIds = [cd for cd in cat_dataIds if cd['filter'] == f]
        dataIds_by_filter[f] = these_dataIds     

    return dataIds_by_filter

def run(field, tract=None):
    repo = os.path.join(os.getenv('DR1BASE'), 'repo', 'test_dr1')
    rerun = os.path.join(repo, 'rerun', 'forcedPhot')

    if tract is None:
        tract = get_tract_for_field(field)

    J_cat, H_cat, ref_table = read_cats(field, tract=tract, repo=rerun)

    snr_threshold = 5
    good_color = (J_cat['J_SNR'] > snr_threshold) & (H_cat['H_SNR'] > snr_threshold)

    J_cat = J_cat[good_color]
    H_cat = H_cat[good_color]
    ref_table = ref_table[good_color]

    butler = Butler(rerun)

    dId = {'field': field, 'filter': 'H', 'tract': tract, 'patch': '0,0'}
    calexp = butler.get('deepCoadd', dataId=dId)

    RA, Dec = get_RA_Dec_for_field(field)

    sn_coord = afwGeom.SpherePoint(RA, Dec, afwGeom.degrees)

    distList = []
    for s in ref_table:
        this_coord = afwGeom.SpherePoint(s['coord_ra'], s['coord_dec'], afwGeom.radians)
        angSep = sn_coord.separation(this_coord)
        distList.append(angSep)

    distance = np.array(distList)
    sn_idx = np.argmin(distance)

    print("Found match: Object %d at %f arcsecs" % (sn_idx, afwGeom.radToArcsec(distance[sn_idx])))

    # Read in the forced-src photometry files that were built off of this same reference table to extract a lightcurve
    dataIds_by_filter = get_dataIds_for_field(butler, field, tract)

    lc = assemble_catalogs_into_lightcurve(dataIds_by_filter, rerun, dataset='forced_src')
    lc_file = '{:s}.ecsv'.format(field)
    lc.write(lc_file, format='ascii.ecsv', overwrite=True)

    lc.pprint(max_width=-1)

def plot(lc, field, ref_table):
    filters = ['J', 'H']
    colors = {'J': 'blue', 'H': 'green', 'KS': 'red'}
    for filt in filters:
        wf, = np.where(lc['filter'] == filt)
        lc_filt = lc[wf]
        plt.errorbar(lc_filt['mjd'], lc_filt['base_PsfFlux_mag'], lc_filt['base_PsfFlux_magSigma'], label=filt,
                    marker='o', color=colors[filt], linestyle='none')

    ylim = plt.ylim()
    plt.ylim(ylim[::-1])

    plt.xlabel('MJD')
    plt.ylabel('mag')
    plt.legend()
    plot_file = '{:s}_lc.pdf'.format(field)

    plt.savefig(plot_file)
    plt.show()

    display = afwDisplay.getDisplay(backend='ds9')

    display.mtv(calexp)

    display.setMaskTransparency(80)
    display.scale("asinh", -2, 25)

    X = 'slot_Centroid_x'
    Y = 'slot_Centroid_y'

    display.erase()

    with display.Buffering():
        for s in ref_table:
            display.dot("o", s[X], s[Y], size=10, ctype='orange')

    sn_ref = ref_table[sn_idx]
    display.dot("o", sn_ref[X], sn_ref[Y], size=20, ctype='green')


if __name__=="__main__":
    field = sys.argv[1]

    field = 'PTF11mty'
    run(field)
