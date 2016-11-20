import glob
import os

from wiynSubtractExp import convname_from_diffname, diffname_from_inputs, subtractFiles
from wiynAssembleExp import makeLsstNamesAndFile

# The following supernovae need host-galaxy subtractions
# and the templates are available as of DR1.
sn_with_dr1_templates = {
     'SN2012fm':                   {'J': 'SN2012fm_A_J_20131018.fits', 'H': 'SN2012fm_A_H_20131018.fits'},
     'PSNJ07250042+2347030':       {'J': 'PSNJ07250042+2347030_A_J_20131213.fits', 'H': 'PSNJ07250042+2347030_A_H_20131213.fits'},
     'LSQ12fuk':                   {'J': 'LSQ12fuk_A_J_20131019.fits', 'H': 'LSQ12fuk_A_H_20131019.fits'},
     'SN2011hb':                   {'J': 'SN2011hb_A_J_20131020.fits', 'H': 'SN2011hb_A_H_20131020.fits'},
#     'PTF11qzq':                   {'J': 'PTF11qzq_A_J_20130925.fits', 'H': 'PTF11qzq_A_H_20121007.fits'},
     'PTF11mty':                   {'J': 'PTF11mty_A_J_20121007.fits', 'H': 'PTF11mty_A_H_20120925.fits'}, 
     'SN2011iu':                   {'J': 'SN2011iu_A_J_20121001.fits', 'H': 'SN2011iu_A_H_20120925.fits'},
     'SN2011gy':                   {'J': 'SN2011gy_A_J_20121028.fits', 'H': 'SN2011gy_A_H_20121028.fits'},
     'PTF11owc':                   {'J': 'PTF11owc_A_J_20120402.fits', 'H': 'PTF11owc_A_H_20121125.fits'}, 
     'SN2011ho':                   {'H': 'SN2011ho_A_H_20120402.fits'}, 
     'PTF11qpc':                   {'H': 'PTF11qpc_A_H_20120402.fits'}, 
    }

repo_dir = os.path.join(os.getenv('HOME'), 'tmp', 'test_dr1')

def find_and_generate_lsst_files(sn):
    """Find the files for a given SN, generate LSST-style fits versions."""
    dr1_dir = os.path.join(os.getenv('DR1BASE'), 'stacks')
    sn_search_regex = os.path.join(dr1_dir, "{}_*[0-9].fits".format(sn))
    files = glob.glob(sn_search_regex)
    for f in files:
        makeLsstNamesAndFile(f) 


def find_science_images(sn, f, repo_dir):
    sn_search_regex = os.path.join(repo_dir, 'calexp', "{}_[ABC]_{}_*[0-9].fits".format(sn, f))
    sn_files = glob.glob(sn_search_regex)
    return sn_files


def test_subtractFiles():
    science_image = 'PS1-12bwh_A_J_20121028.fits'
    template_image = 'PS1-12bwh_A_J_20121130.fits'
    out_image = 'PS1-12bwh_A_J_20121028_20121130.diff.fits'

    scienceImage = os.path.join(repo_dir, 'calexp', science_image)
    templateImage = os.path.join(repo_dir, 'calexp', template_image)
    diff_file = diffname_from_inputs(os.path.basename(science_file),
                                     os.path.basename(template_file))
    conv_file = convname_from_diffname(os.path.basename(diff_file))
    subtractFiles(science_file, template_file, diff_file, conv_file)


def filename_to_fileroot(filename):
    fileroot = os.path.basename(filename)
    fileroot = fileroot.replace('.lsst.fits', '')
    fileroot = fileroot.replace('.fits', '')
    return fileroot


def run_repo_based_subtraction(science_file, template_file, repo_dir, verbose=True):
    """Run a subtraction using the Butler"""
    science_fileroot = filename_to_fileroot(science_file)
    template_fileroot = filename_to_fileroot(template_file)
    args = [repo_dir,
            '--id', 'fileroot={}'.format(science_fileroot),
            '--templateId', 'fileroot={}'.format(template_fileroot),
            '--output', repo_dir,
            '--configfile', 'diffimconfig.py',
            '--clobber-config', '--clobber-versions',
           ]
    from lsst.pipe.tasks.imageDifference import ImageDifferenceTask

    if verbose:
        print("Running ImageDifferenceTask.parseAndrun with args:")
        print(args)
    ImageDifferenceTask.parseAndRun(args=args)


def run_file_based_subtraction(science_file, template_file):
    """Run a subtraction just based on file names, write output to POSIX file system."""
    diff_file = diffname_from_inputs(science_file, template_file)
    conv_file = convname_from_diffname(diff_file)
    print("subtractFiles({}, {}, {}, {})".format(science_file, template_file, diff_file, conv_file))
    try:
        subtractFiles(science_file, template_file, diff_file, conv_file)
    except Exception as e:
        print(e)


if __name__ == "__main__":
#    for sn in sn_with_dr1_templates:
#        find_and_generate_lsst_files(sn)

    # Do we run subtraction directly from files
    # or use the repo-based Butler interface
    repo_based = True

    for name, templates in sn_with_dr1_templates.items():
        print("Processing {}".format(name))
        for f in templates.keys():
            template_file = os.path.join(repo_dir, 'calexp', templates[f])
            for science_file in find_science_images(name, f, repo_dir):
                if science_file == template_file:
                    continue
                if repo_based:
                    run_repo_based_subtraction(science_file, template_file, repo_dir)
                else:
                    run_file_based_subtraction(science_file, template_file)

