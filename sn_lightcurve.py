import os
import sys

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


def get_RA_Dec_for_target(target,
                          sn_info_file='observed_target_info.dr1.txt',
                          twomass_info_file='2MASS_DR1_stars.txt'):
    """Return RA, Dec in decimal degrees for specified target."""
    sn_info = read_in_DR1_targets(sn_info_file)

    w, = np.where(sn_info['Name'] == target)
    if len(w) > 0:
        target_info = sn_info[w]
        # Want scalars rather than 1-element lists
        ra, dec = target_info['RA'][0], target_info['Dec'][0]
        # Target catalog in sexagesimal hours, degrees
        coord = SkyCoord(ra, dec, unit=(u.hour, u.deg))
    else:
        twomass_info = read_in_2MASS_data(twomass_info_file)
        number_only_twomass_id = target[-16:]
        w, = np.where(twomass_info['2MASSID'] == number_only_twomass_id)
        target_info = twomass_info[w]
        # Want scalars rather than 1-element lists
        ra, dec = target_info['RA'][0], target_info['Dec'][0]
        # 2MASS catalog in decimal degrees
        coord = SkyCoord(ra, dec, unit=(u.deg, u.deg))

    return coord.ra.to(u.deg).value, coord.dec.to(u.deg).value


def read_in_DR1_targets(file='observed_target_info.dr1.txt'):
    return Table.read(file, format='ascii.commented_header')


def read_in_2MASS_data(filename, debug=False):
    """Read in CSV file of catalog

    #RA DEC 2MASSID Jmag eJmag Hmag eHmag Kmag eKmag
    060.877901;-02.709703;04033069-0242349 ;13.922; 0.028;13.449; 0.032;13.303; 0.038
    060.921678;-02.695895;04034120-0241452 ;14.831; 0.035;14.174; 0.037;13.975; 0.054
    060.903753;-02.706162;04033690-0242221 ;15.905; 0.082;15.553; 0.114;15.226; 0.152
    """
    colnames = ('RA', 'Dec', '2MASSID',
                'Jmag', 'eJmag', 'Hmag', 'eHmag', 'Kmag', 'eKmag')
    data = Table.read(filename, format='csv', delimiter=';', data_start=1, names=colnames)
    if debug:
        print(data)

    return data

def get_dataIds_for_field(butler, field, tract=None, seq='A', patch='0,0',
                          datasetType='forced_src'):
    """Lookup available forced source in Butler."""
    if tract is None:
        tract = get_tract_for_field(field)

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


def make_lc(field, target=None, tract=None, do_snr_cut=False, verbose=True):
    """Extract a lightcurve from the calexps for the given field, target.

    If target is None, then field name is used as the target.
    """
    repo = os.path.join(os.getenv('DR1BASE'), 'repo', 'test_dr1')
    rerun = os.path.join(repo, 'rerun', 'forcedPhot')

    if target is None:
        target = field

    if tract is None:
        tract = get_tract_for_field(field)

    ref_table, cats = read_cats(field, tract=tract, repo=rerun)

    if do_snr_cut:
        snr_threshold = 5
        good = [True for i in range(len(ref_table))]
        for cat in cats:
            filt = cat.meta['filter']
            these_good = cat['%s_SNR' % filt] > snr_threshold
            good = good & these_good

        ref_table = ref_table[good]
        for cat in cats:
            cat = cat[good]

    RA, Dec = get_RA_Dec_for_target(target)
    if verbose:
        print("Making lightcurve for %s at (RA, Dec)=(%f, %f)" %
              (target, RA, Dec))

    target_coord = afwGeom.SpherePoint(RA, Dec, afwGeom.degrees)

    distList = []
    for s in ref_table:
        this_coord = afwGeom.SpherePoint(s['coord_ra'], s['coord_dec'], afwGeom.radians)
        angSep = target_coord.separation(this_coord)
        distList.append(angSep)

    distance = np.array(distList)
    target_idx = np.argmin(distance)

    print('Found match: Object %d at %f arcsecs' %
          (target_idx, afwGeom.radToArcsec(distance[target_idx])))

    # Extract a lightcurve by reading in the forced-src photometry files
    # that were built off of this same reference table.
    butler = Butler(rerun)
    dataIds_by_filter = get_dataIds_for_field(butler, field, tract)

    lc = assemble_catalogs_into_lightcurve(dataIds_by_filter, rerun, dataset='forced_src')
    lc_file = '{:s}_{:s}.ecsv'.format(field, target)
    lc.write(lc_file, format='ascii.ecsv', overwrite=True)

    lc.pprint(max_width=-1)

    return butler, lc, ref_table, target_idx


def plot_lc(lc, field, show=False):
    import matplotlib.pyplot as plt

    filters = ['J', 'H']
    colors = {'J': 'blue', 'H': 'green', 'KS': 'red'}
    for filt in filters:
        wf, = np.where(lc['filter'] == filt)
        lc_filt = lc[wf]
        plt.errorbar(lc_filt['mjd'], lc_filt['base_PsfFlux_mag'], lc_filt['base_PsfFlux_magSigma'],
                     label=filt,
                     marker='o', color=colors[filt], linestyle='none')

    ylim = plt.ylim()
    plt.ylim(ylim[::-1])

    plt.xlabel('MJD')
    plt.ylabel('mag')
    plt.legend()
    plot_file = '{:s}_lc.pdf'.format(field)

    plt.savefig(plot_file)
    if show:
        plt.show()


def show_cat(butler, lc, ref_table, target_idx, field, tract=None):
    if tract is None:
        tract = get_tract_for_field(field)

    dId = {'field': field, 'filter': 'H', 'tract': tract, 'patch': '0,0'}
    calexp = butler.get('deepCoadd', dataId=dId)

    display = afwDisplay.getDisplay(backend='ds9')

    display.mtv(calexp)

    display.setMaskTransparency(80)
    display.scale('asinh', -2, 25)

    X = 'slot_Centroid_x'
    Y = 'slot_Centroid_y'

    display.erase()

    with display.Buffering():
        for s in ref_table:
            display.dot('o', s[X], s[Y], size=10, ctype='orange')

    target_ref = ref_table[target_idx]
    display.dot('o', target_ref[X], target_ref[Y], size=20, ctype='green')


def process_target(field, target, doPlot=False, doShow=False):
        try:
            butler, lc, ref_table, target_idx = make_lc(field, target)
        except Exception as e:
            print('Could not generate a LC for "%s":' % target)
            print(e)

        if doPlot:
            # We borrow the image version to show the plot
            # if show=False they we would just generate a PDF.
            plot_lc(lc, target, show=doShow)
        if doShow:
            show_cat(butler, lc, ref_table, target_idx, target)


def parse_and_run(fields, targets=None, **kwargs):
    if targets is None:
        targets = fields.copy()

    for field, target in zip(fields, targets):
        process_target(field, target, **kwargs)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Make lightcurve.')
    parser.add_argument('field', metavar='FIELD', type=str, nargs='+')
    parser.add_argument('--target', type=str, nargs='+',
                        help='Specify a different target name than the field name.  Must have some number of entries as field.')
    parser.add_argument('--doPlot', default=False, action='store_true',
                        help='Plot the lightcurve.  If doShow is set also display.')
    parser.add_argument('--doShow', default=False, action='store_true',
                        help='Show the coadd, coadd catalog, and matched target object.')

    args = parser.parse_args(sys.argv[1:])

    parse_and_run(args.field, targets=args.target,
                  doPlot=args.doPlot, doShow=args.doShow)
