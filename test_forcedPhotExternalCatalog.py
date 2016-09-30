#!/usr/bin/env python
import os

from sub_wiyn_dr1 import sn_with_dr1_templates, repo_dir, find_science_images, filename_to_fileroot
import forcedPhotExternalCatalog

def run_forced_photometry(science_file, template_file, coord_file, repo_dir):
    science_fileroot = filename_to_fileroot(science_file)
    args = [repo_dir,
            '--id', 'fileroot="{}"'.format(science_fileroot),
            '--coord_file', '"{}"'.format(coord_file),
            '--output "{}"', repo_dir,
            '--logdest', 'wiyn_imagePhotometry.log',
            '--clobber-config', '--clobber-versions',
           ]
    forcedPhotExternalCatalog.parseAndRun(args=args)


if __name__ == "__main__":
    for name, sn in sn_with_dr1_templates.items():
        coord_file = '{}_ra_dec.txt'.format(name)

        print("Processing photometry for {}".format(name))
#        for f in sn.keys():
        for f in 'H':
            template_file = os.path.join(repo_dir, 'calexp', sn[f])
            for science_file in find_science_images(name, f, repo_dir):
                if science_file == template_file:
                    continue
                run_forced_photometry(science_file, template_file, coord_file, repo_dir)
