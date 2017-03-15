import glob
import os
import sys
import ast

from wiynSubtractExp import convname_from_diffname, diffname_from_inputs, subtractFiles
from wiynAssembleExp import makeLsstNamesAndFile

# The following supernovae need host-galaxy subtractions
with open('template_dictionary.txt','r') as inf:
    sn_with_dr2_templates = ast.literal_eval(inf.read())


repo_dir = os.path.join(os.getenv('HOME'), 'tmp', 'test_dr1')

def find_and_generate_lsst_files(sn):
    """Find the files for a given SN, generate LSST-style fits versions."""
    dr1_dir = os.path.join(os.getenv('DR2BASE'), 'stacks')
    sn_search_regex = os.path.join(dr1_dir, "{}_*[0-9].fits".format(sn))
    files = glob.glob(sn_search_regex)
    for f in files:
        makeLsstNamesAndFile(f) 


def find_science_images(sn, f, repo_dir, dataset='calexp', verbose=False):
    if dataset == 'deepDiff_differenceExp':
        search_dataset = 'diff'
        suffix = ''
    elif dataset == 'calexp':
        search_dataset = dataset
        suffix = '.fits'
    else:
        search_dataset = dataset
        suffix = ''

    sn_search_regex = os.path.join(repo_dir, search_dataset, "{}_[ABC]_{}_*[0-9]{}".format(sn, f, suffix))
    if verbose:
        print("Searching for: ", sn_search_regex)
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

    repo_dir = sys.argv[1]
    for name, templates in sn_with_drs_templates.items():
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


