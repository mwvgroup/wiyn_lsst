#!/usr/bin/env python

# File:  Wstd.py
# Date Created:  2005 May 13
# Last Changed:  2014 Aug 22
#
# Purpose:  This file contains the input and output routines
#  for the agreed-upon standard ESSENCE formats.
#
#  Attempted to merge two forks of Wstd.py on 2014-08-22

from __future__ import division, print_function

import re

import numpy as np

verbose = False


def nfloat(arg):
    try:
        return float(arg)
    except:
        return None


def normflux25(flux, zp, zpnorm=25):
    return flux * 10**(-0.4*(zp-zpnorm))


def mag2flux(mag, zpnorm=25):
    return 10**(-0.4*(mag-zpnorm))


def magerr2fluxerr(mag, magerr, zpnorm=25):
    fluxerr = abs(mag2flux(mag+magerr, zpnorm=zpnorm) -
                  mag2flux(mag, zpnorm=zpnorm))
    return fluxerr


def mag(flux, zp=25):
    return -2.5*np.log10(flux)+zp


# Return string representation of float or return '---' if 'f' is None
# with 4-digit decimal precision
def float2str(f):
    if f is None:
        fstr = '---'
    else:
        fstr = "%6.4f" % float(f)

    return fstr


# Calculate symmetric magnitude error [shudder]
def magerr(flux, fluxerr, zp=25):
    symmetric_magerr = (mag(flux-fluxerr, zp) - mag(flux+fluxerr, zp)) / 2
    return symmetric_magerr


# 2008/03/15 - MWV:  I'm sure this class has been written many times before
#   and will be written many times again
# A quick Google search doesn't bring up anything good
#   or any hooks into larger frameworks that solve many of the issues
class LC:
    def __init__(self, mjd, passband, flux, dflux, dflux_hi,
                 zeropoint=None, observation=None):
        default_zp = 25

        if observation is not None:
            self.observation = observation
        else:
            self.observation = [None for i in mjd]

        self.mjd = np.asarray(mjd)
        self.passband = np.asarray(passband)
        self.flux = np.asarray(flux)
        self.dflux_lo = np.asarray(dflux)
        if dflux_hi:
            self.dflux_hi = np.asarray(dflux_hi)
        else:
            self.dflux_hi = self.dflux_lo
        # And the average
        self.dflux = (self.dflux_hi + self.dflux_lo)/2.

        self.dflux = (self.dflux_lo + self.dflux_hi)/2.

        if zeropoint is None:
            self.zp = np.asarray([default_zp for i in mjd])
        else:
            self.zp = np.asarray(zeropoint)


class rawLC:
    def __init__(self, mjd, passband, flux, flux_err, mag, mag_sig, peakflux,
                 sky, zp, exptime, x_psf, y_psf, ra_psf, dec_psf, file):

        self.mjd = mjd
        self.passband = passband
        self.flux = flux
        self.flux_err = flux_err
        self.mag = mag
        self.mag_sig = mag_sig
        self.peakflux = peakflux
        self.sky = sky
        self.zp = zp
        self.exptime = exptime
        self.x_psf = x_psf
        self.y_psf = y_psf
        self.ra_psf = ra_psf
        self.dec_psf = dec_psf
        self.file = file

        self.dflux_lo = flux_err
        self.dflux_hi = flux_err


class Wstd:
    def __init__(self):
        self.WstdLCsuffix = "Wstd.dat"

    # Stores the SN-parameter contents of a header
    class WstdHeader:
        def __init__(self,
                     sn=None, l=None, b=None, MW_E_BmV=None,
                     z_hel=None, z_cmb=None, RA=None, Dec=None,
                     comments=None):
            self.sn = sn
            self.l = l
            self.b = b
            self.MW_E_BmV = nfloat(MW_E_BmV)
            self.z_hel = nfloat(z_hel)
            self.z_cmb = nfloat(z_cmb)
            self.RA = RA
            self.Dec = Dec
            self.comments = comments

        def __repr__(self):
            # Take a plain redshift as the heliocentric redshift
            # Format strings appropriately
            RAstr = '---'
            Decstr = '---'
            lIIstr = '---'
            bIIstr = '---'
            eventstr = self.sn
            MW_E_BmVstr = float2str(self.MW_E_BmV)
            z_helstr = float2str(self.z_hel)
            z_cmbstr = float2str(self.z_cmb)

            header = "#  %10s %10s %10s %10s %10s %10s %15s %15s\n" % \
                (eventstr, lIIstr, bIIstr, MW_E_BmVstr, z_helstr, z_cmbstr, RAstr, Decstr)

            return header

    def readLightcurve(self, file, datamag=False):
        observation = []
        mjd = []
        passband = []
        flux = []
        dflux_low = []
        dflux_high = []

        for line in open(file).readlines():
            if re.match('^\s*#', line):
                continue
            if not re.match('[-/ a-zA-Z0-9]', line):
                continue

            (o, m, p, f, dfl, dfh) = (line.strip().split())[0:6]

            observation.append(o)
            mjd.append(float(m))
            passband.append(p)
            if datamag:
                flux.append(mag2flux(float(f)))
                dflux_low.append(magerr2fluxerr(float(f,), -float(dfl)))
                dflux_high.append(magerr2fluxerr(float(f), +float(dfh)))
            else:
                flux.append(float(f))
                dflux_low.append(float(dfl))
                dflux_high.append(float(dfh))
            if verbose:
                print(line)

        return LC(mjd, passband, flux, dflux_low, dflux_high, observation=observation)

    def writeLightcurve(self, file, sninfo, data):
        pass

    def formatWstdColumnHeader(self):
        return "#%-49s %-12s %20s %12s %25s\n" % ("Observation", "MJD", "Passband", "Flux", "Fluxerr (- +)")
#         return "#%-49s %-12s %20s %12s %12s %12s\n" % \
#             ("Observation", "MJD", "Passband", "Flux", "Fluxerr_lo", "Fluxerr_hi")

    def formatWstdLine(self, observation, mjd, filter, flux, fluxerrL, fluxerrH=None):
        # If passed just one error then assume symmetric and duplicate
        if fluxerrH is None:
            fluxerrH = fluxerrL

        # Format the line and return it
        line = "%-50s %-14.6f %20s %12.4f %12.4f %12.4f\n" % \
            (observation, float(mjd), filter, float(flux), float(fluxerrL), float(fluxerrH))
        return line

    def formatWstdData(self, observation, mjd, passband, flux, fluxerr_low, fluxerr_high=None,
                       zp=25, SNthreshold=None, suffix=None):
        if fluxerr_high is None:
            fluxerr_high = fluxerr_low
        if len(passband) == -1:
            filters = [passband for i in range(len(mjd))]
        else:
            filters = passband

        datastr = ''
        for (o, m, p, f, dfl, dfh) in zip(observation, mjd, filters, flux, fluxerr_low, fluxerr_high):
            if not (dfl > 0 and dfh > 0):
                continue
            if not (np.isfinite(f) and np.isfinite(dfl) and np.isfinite(dfh)):
                continue
            if suffix is not None and isinstance(o, str) and not re.match(suffix, o):
                o += "_"+suffix
            # Reject flux points < SNthreshold if called
            if SNthreshold and f/fluxerr_low < SNthreshold:
                continue
            datastr += self.formatWstdLine(o, m, p, f, dfl, dfh)
        return datastr

    def formatWstdLC(self, *args, **kwargs):
        datastr = ''
        datastr += self.formatWstdColumnHeader()
        datastr += self.formatWstdData(*args, **kwargs)
        return datastr

    # Can accept either spelled-out
    def formatWstdHeader(self, event, RA=None, Dec=None, MW_E_BmV=None,
                         z=None, z_hel=None, z_cmb=None,
                         lII=None, bII=None, extraHeaderInfo=''):
        # Take a plain redshift as the heliocentric redshift
        if z_hel is None:
            z_hel = z
        # Format strings appropriately
        RAstr = '---'
        Decstr = '---'
        lIIstr = '---'
        bIIstr = '---'
        try:
            if RA is not None:
                RAstr = str(RA)
            if Dec is not None:
                Decstr = str(Dec)
            if lII is not None:
                lIIstr = str(lII)
            if bII is not None:
                bIIstr = str(bII)
        except:
            pass

        eventstr = str(event)
        MW_E_BmVstr = float2str(MW_E_BmV)
        z_helstr = float2str(z_hel)
        z_cmbstr = float2str(z_cmb)

        header = ""
        header += "#  %-30s %10s %10s %10s %10s %10s %31s\n" % \
            ("Event", "lII", "bII", "MW_E(B-V)", "z (helio)", "z (CMB)", "R.A. (2000.0) Decl.")
        header += "#  %-30s %10s %10s %10s %10s %10s %15s %15s\n" % \
            (eventstr, lIIstr, bIIstr, MW_E_BmVstr, z_helstr, z_cmbstr, RAstr, Decstr)
        header += \
"""# *************************************************************************************************
#
"""
        header += extraHeaderInfo
        header += """
#
# 'Flux', 'Fluxerr_lo', 'Fluxerr_hi' normalized to a zeropoint of 25.
#   I.e., mag = -2.5*log10(flux) + 25.
#   (This is merely a convention and is completely separate from the question of calibration.)
# To clarify:  Flux+Fluxerr_hi is one sigma above the nominal value and
#              Flux-Fluxerr_lo is one sigma below the nominal value
#
# 'Observation' is supposed to be the full information about a given observation.
#
"""
        return header

    def readWstdHeader(self, file):
        try:
            lines = open(file).readlines()
        except:
            print("Couldn't open file ", file)

        cleanedline = lines[1].strip('#').replace("[", "").replace("]", "").strip()
        temparr = cleanedline.split()
        # Handle cases where only one redshift is given and new format with both z_Heliocentric and z_CMB
        if len(temparr) == 8:
            (sn, l, b, MW_E_BmV, z_hel, z_cmb, RA, Dec) = temparr
        elif len(temparr) == 7:
            (sn, l, b, MW_E_BmV, z_hel, RA, Dec) = temparr
            z_cmb = '---'
        else:
            print("Couldn't parse header of file: ", file)
            print("Is this file in Wstd format?")
            print("Returning blank header object")
            return self.WstdHeader()

        comments = ''
        i = 4
        lastline = lines[i]
        i += 1
        line = lines[i]
        comment = re.compile('\s*#')
        while comment.match(line):
            comments += lastline
            i += 1
            lastline = line
            line = lines[i]

        # Format strings to None, strings or floats as appropriate
        if sn == '---':
            sn = None
        if l == '---':
            l = None
        if b == '---':
            b = None
        if MW_E_BmV == '---':
            MW_E_BmV = None
        if z_hel == '---':
            z_hel = None
        if z_cmb == '---':
            z_cmb = None

        return self.WstdHeader(sn, l, b, MW_E_BmV, z_hel, z_cmb, RA, Dec,
                               comments=comments)


class Raw:
    def __init__(self):
        self.RawLCsuffix = ".raw.dat"

    # Stores the SN-parameter contents of a header
    class RawHeader:
        def __init__(self, comments=None):
            self.comments = comments

        def __repr__(self):
            # Take a plain redshift as the heliocentric redshift
            # Format strings appropriately
            RAstr = '---'
            Decstr = '---'
            lIIstr = '---'
            bIIstr = '---'
            eventstr = self.sn
            MW_E_BmVstr = float2str(self.MW_E_BmV)
            z_helstr = float2str(self.z_hel)
            z_cmbstr = float2str(self.z_cmb)

            header = "#  %10s %10s %10s %10s %10s %10s %15s %15s\n" % \
                (eventstr, lIIstr, bIIstr, MW_E_BmVstr, z_helstr, z_cmbstr, RAstr, Decstr)

            return header

    def readLightcurve(self, file, datamag=False):
        # We're reading a lightcurve of the form
        # MJD-OBS, FILTER, FLUX25, FLUX25_ERR, CAL_PSF_MAG, MAG_SIG, PEAKFLUX, \
        #    SKY, ZP+2.5log(T), EXPTIME, X_PSF, Y_PSF, RA_PSF, DEC_PSF, FILE
        mjd = []
        passband = []
        flux = []
        flux_err = []
        mag = []
        mag_sig = []
        peakflux = []
        sky = []
        zp = []
        exptime = []
        x_psf = []
        y_psf = []
        ra_psf = []
        dec_psf = []
        files = []

        # This is all a little silly.  I feel that I should use asciitable, or at least numpy.genfromtxt.
        print("File: ", file)
        for line in open(file).readlines():
            if re.match('^\s*#', line):
                continue
            if not re.match('[- a-zA-Z0-9]', line):
                continue

            (m, p, f25, f25err, ma, me, pk, s, zp, expt, x, y, ra, dec, fil) = line.strip().split()
            mjd.append(float(m))
            passband.append(p)
            flux.append(float(f25))
            flux_err.append(float(f25err))
            mag.append(float(ma))
            mag_sig.append(float(me))
            peakflux.append(float(pk))
            sky.append(float(s))
            exptime.append(float(expt))
            x_psf.append(float(x))
            y_psf.append(float(y))
            ra_psf.append(float(ra))
            dec_psf.append(float(dec))
            files.append(fil)

            if verbose:
                print(line)

        return rawLC(mjd, passband, flux, flux_err, mag, mag_sig, peakflux,
                     sky, zp, exptime, x_psf, y_psf, ra_psf, dec_psf, files)

    def writeLightcurve(self, file, sninfo, data):
        pass

    def formatRawColumnHeader(self):
        return "#%-49s %-12s %20s %12s %25s\n" % \
            ("Observation", "MJD", "Passband", "Flux", "Fluxerr (- +)")
#         return "#%-49s %-12s %20s %12s %12s %12s\n" % \
#             ("Observation", "MJD", "Passband", "Flux", "Fluxerr_lo", "Fluxerr_hi")

    def formatRawLine(self, observation, mjd, filter, flux, fluxerrL, fluxerrH=None):
        # If passed just one error then assume symmetric and duplicate
        if fluxerrH is None:
            fluxerrH = fluxerrL

        # Format the line and return it
        line = "%-50s %-14.6f %20s %12.4f %12.4f %12.4f\n" % \
            (observation, float(mjd), filter, float(flux), float(fluxerrL), float(fluxerrH))
        return line

    def formatRawData(self, observation, mjd, passband, flux, fluxerr_low, fluxerr_high=None,
                      zp=25, SNthreshold=None):
        if fluxerr_high is None:
            fluxerr_high = fluxerr_low
        if len(passband) == -1:
            filters = [passband for i in range(len(mjd))]
        else:
            filters = passband

        datastr = ''
        for (o, m, p, f, dfl, dfh) in zip(observation, mjd, filters, flux, fluxerr_low, fluxerr_high):
            if not (dfl > 0 and dfh > 0):
                continue
            if not (np.isfinite(f) and np.isfinite(dfl) and np.isfinite(dfh)):
                continue
            # Reject flux points < SNthreshold if called
            if SNthreshold and f/fluxerr_low < SNthreshold:
                continue
            datastr += self.formatRawLine(o, m, p, f, dfl, dfh)
        return datastr

    def formatRawLC(self, *args, **kwargs):
        datastr = ''
        datastr += self.formatRawColumnHeader()
        datastr += self.formatRawData(*args, **kwargs)
        return datastr

    def formatRawHeader(self, event, RA=None, Dec=None, lII=None, bII=None, MW_E_BmV=None,
                        z=None, z_hel=None, z_cmb=None, extraHeaderInfo=''):
        # Take a plain redshift as the heliocentric redshift
        if z_hel is None:
            z_hel = z
        # Format strings appropriately
        RAstr = '---'
        Decstr = '---'
        lIIstr = '---'
        bIIstr = '---'
        try:
            if RA is not None:
                RAstr = str(RA)
            if Dec is not None:
                Decstr = str(Dec)
            if lII is not None:
                lIIstr = str(lII)
            if bII is not None:
                bIIstr = str(bII)
        except:
            pass

        eventstr = str(event)
        MW_E_BmVstr = float2str(MW_E_BmV)
        zstr = float2str(z)
        z_helstr = float2str(z_hel)
        z_cmbstr = float2str(z_cmb)

        header = ''
        header += "#  Event      lII     bII    MW_E(B-V)   z       R.A. (2000.0) Decl.\n"
        header += "#  %s    %s     %s    %6s     %6s      %s           %s\n" % \
            (eventstr, lIIstr, bIIstr, MW_E_BmVstr, zstr, RAstr, Decstr)
        header += "#  %10s %10s %10s %10s %10s %10s %31s\n" % \
            ("Event", "lII", "bII", "MW_E(B-V)", "z (helio)", "z (CMB)", "R.A. (2000.0) Decl.")
        header += "#  %10s %10s %10s %10s %10s %10s %15s %15s\n" % \
            (eventstr, lIIstr, bIIstr, MW_E_BmVstr, z_helstr, z_cmbstr, RAstr, Decstr)
        header += """
# *************************************************************************************************
# The values above aren't all filled in yet.
#
#
# 'Flux', 'Fluxerr_lo', 'Fluxerr_hi' normalized to a zeropoint of 25.
# To clarify:  Flux+Fluxerr_hi is one sigma above the nominal value and
#              Flux-Fluxerr_lo is one sigma below the nominal value
#
# 'Observation' is supposed to be the full information about a given observation,
#   but is currently just the filename.
#
"""
        return header

    def readRawHeader(self, file):
        try:
            lines = open(file).readlines()
        except:
            print("Couldn't open file ", file)

        temparr = lines[1].strip('#').strip().split()
        # Handle cases where only one redshift is given and new format with both z_Heliocentric and z_CMB
        if len(temparr) == 8:
            (sn, l, b, MW_E_BmV, z_hel, z_cmb, RA, Dec) = temparr
        elif len(temparr) == 7:
            (sn, l, b, MW_E_BmV, z_hel, RA, Dec) = temparr
            z_cmb = '---'
        else:
            print("Couldn't parse header of file: ", file)
            print("Is this file in Raw format?")
            print("Returning blank header object")
            return self.RawHeader()

        comments = ''
        i = 4
        lastline = lines[i]
        i += 1
        line = lines[i]
        comment = re.compile('\s*#')
        while comment.match(line):
            comments += lastline
            i += 1
            lastline = line
            line = lines[i]

        # Format strings to None, strings or floats as appropriate
        if sn == '---':
            sn = None
        if l == '---':
            l = None
        if b == '---':
            b = None
        if MW_E_BmV == '---':
            MW_E_BmV = None
        if z_hel == '---':
            z_hel = None
        if z_cmb == '---':
            z_cmb = None

        return self.RawHeader(sn, l, b, MW_E_BmV, z_hel, z_cmb, RA, Dec,
                              comments=comments)

