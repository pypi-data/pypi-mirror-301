import os
import numpy as np
from mocpy import MOC, WCS
from astropy import units as u
from astropy.coordinates import Angle, SkyCoord


def fastFeatureExtractor(objectset, logger):

    # load in the list of MOC files
    try:
        moc_files = [files for files in os.listdir('fastfinder/MOCs') if os.path.isfile(os.path.join('fastfinder/MOCs', files) ) ]
    except:
        moc_files = []
    MOCs = {}
    for filename in moc_files:
        moc_filebody = filename.replace('.fits','')
        MOCs[moc_filebody] = MOC.load(f'fastfinder/MOCs/'+filename, 'fits')
    
    # extract features from the objects in the list of objects
    for object in objectset:

        # Cosmological parameters
        c = 300000.0    # Speed of light in km/s
        Ho = 70.0       # Hubble constant in Km/s/Mpc
        Hoerr = 3.0    # Hubble constant uncertainty

        normz = object['sherlock']['hostz']
        diridst = object['sherlock']['hostdirectdistance']
        dirdisterr = (5/100) * diridst # 5% of the direct distance
        reddist = object['sherlock']['hostdistance']
        reddisterr = (5/100) * reddist # 5% of the redshift distance
        photz = object['sherlock']['hostphotz']
        photzerr = object['sherlock']['hostphotzerr']

        # Determine the distance modulus from the Sherlock distance or redshift
        if diridst != 0.0:
            dist_mod = 5*np.log10(diridst*1E6) - 5
            dist_mod_err = np.log(10)*(dirdisterr/diridst)
        elif reddist != 0.0:
            dist_mod = 5*np.log10(reddist*1E6) - 5
            dist_mod_err = np.log(10)*(reddisterr/reddist)
        elif photz != 0.0:
            photdist = ( (photz * c) / Ho)
            photdisterr = photdist * ( (photzerr/photz)**2 + (Hoerr/Ho)**2) ** 0.5
            dist_mod = 5*np.log10(photdist*1E6) - 5
            dist_mod_err = np.log(10)*(photdisterr/photdist)
        else:
            normz = ''
            photz = ''
            photzerr = ''
            dist_mod = ''
            dist_mod_err = ''
        object['objectData']['z'] = normz
        object['objectData']['photoZ'] = photz
        object['objectData']['dphotoZ'] = photzerr
        object['objectData']['m-M'] = dist_mod
        object['objectData']['dm-M'] = dist_mod_err

        # list the model singleband lightcurves
        object_lc_list = object['lightcurve']['model_singlebands']
  
        # iterate through each of the singleband lightcurves and extract lightcurve features
        for singleband, lightcurve in object_lc_list.items():
            
            if len(lightcurve) > 0:

                # calculate peak absolute brightness
                abs_mag, abs_mag_err = extractAbsoluteMag(lightcurve, dist_mod, dist_mod_err)
                object['lightcurve']['features'][singleband]['absolute_peak_mag_val'] = abs_mag
                object['lightcurve']['features'][singleband]['absolute_peak_mag_err'] = abs_mag_err

                # calculate overall incline rate from first epoch to peak
                incline_rate, incline_rate_err = extractGeneralRate(lightcurve, 'incline')
                object['lightcurve']['features'][singleband]['overall_incline_rate_val'] = incline_rate
                object['lightcurve']['features'][singleband]['overall_incline_rate_err'] = incline_rate_err

                # calculate overall delcine rate from peak to latest epoch
                decline_rate, decline_rate_err = extractGeneralRate(lightcurve, 'decline')
                object['lightcurve']['features'][singleband]['overall_decline_rate_val'] = decline_rate
                object['lightcurve']['features'][singleband]['overall_decline_rate_err'] = decline_rate_err
        
        # use both the raw and modelled lightcurves to extract colours
        object['lightcurve']['features']['colours'] = {}
        
        # first attempt g-r colour
        if 'lsst-g' in object['lightcurve']['model_singlebands']:
            g_model_lc = object['lightcurve']['model_singlebands']['lsst-g']
        else:
            g_model_lc = []
        if 'lsst-r' in object['lightcurve']['model_singlebands']:
            r_model_lc = object['lightcurve']['model_singlebands']['lsst-r']
        else:
            r_model_lc = []
        # function expects blue filter first (raw then model) then red filter (raw then model)
        g__r_val, g__r_err = extractLatestColour(object['lightcurve']['raw_singlebands']['lsst-g'], g_model_lc, object['lightcurve']['raw_singlebands']['lsst-r'], r_model_lc)
        object['lightcurve']['features']['colours']['latest_g_minus_r_val'] = g__r_val
        object['lightcurve']['features']['colours']['latest_g_minus_r_err'] = g__r_err
        
        # iterate through the TNS info for each object if it exists and extract the most useful info to stick into the features dictionary
        if bool(object['tns']):
            tns_dict = formatTNSinfo(object['tns'])
            object['lightcurve']['features']['tns'] = tns_dict
        else:
            object['lightcurve']['features']['tns'] = {}

        # check if the object is associated with the glactic plane or other major extragalactic bodies and stick into the features dictionary
        object['lightcurve']['features']['in-major-body'] = coincidesMajorMody(object['objectData'], MOCs)

    return objectset



def extractAbsoluteMag(lightcurve, dist_mod, dist_mod_err):

    # list out the data components
    mags = lightcurve[1]
    errs = lightcurve[2]

    # find the value of mag at maximum light
    peak_mag = min(mags)
    peak_idx = mags.index(peak_mag)
    peak_magerr = errs[peak_idx]

    # calculate peak mag if there is a distance modulus
    # elese set the peak mag to 'unknown'
    if dist_mod != '':
        absmag = round(peak_mag - dist_mod, 3)
        absmag_err = round(((peak_magerr**2) + (dist_mod_err**2))**0.5, 3)
    else:
        absmag = 'unknown'
        absmag_err = 'unknown'

    return absmag, absmag_err

                 

def extractGeneralRate(lightcurve, rateform):

    # list out the data components
    phase = lightcurve[0]
    mags = lightcurve[1]
    errs = lightcurve[2]
    
    # find the values of mag and phase at maximum light
    peak_mag = min(mags)
    peak_idx = mags.index(peak_mag)
    peak_phase = phase[peak_idx]
    peak_err = errs[peak_idx]
    

    # find the values of the mag and phase before or after maximum light
    if rateform == 'incline':
        dayspan_idx = 0
    elif rateform == 'decline':
        dayspan_idx = -1
    dayspan_mag = mags[dayspan_idx]
    dayspan_phase = phase[dayspan_idx]
    dayspan_err = errs[dayspan_idx]

    # calculate incline/decline rate and error if applicable
    if peak_phase != dayspan_phase:
        dt = abs(peak_phase - dayspan_phase)
        dm = abs(peak_mag - dayspan_mag)
        dm_err = ((peak_err**2) + (dayspan_err**2))**0.5
        
        if dt > 0.125:
            dmdt = round(dm/dt, 3)
            dmdt_err = round((dm_err / dm) * dmdt, 3)
        else:
            dmdt = 'unknown'
            dmdt_err = 'unknown'
    else:
        dmdt = 'unknown'
        dmdt_err = 'unknown'

    return dmdt, dmdt_err



def extractLatestColour(blue_raw_lc, blue_model_lc, red_raw_lc, red_model_lc):

    # if any filter is absent a colour cannot be measured
    if len(blue_raw_lc) == 0 or len(red_raw_lc) == 0:
        blue_minus_red_val = 'unknown'
        blue_minus_red_err = 'unknown'
    else:
        
        #
        if len(blue_model_lc) > 0:
            blue_latest_phase = blue_model_lc[0][-1]
            blue_latest_magvl = blue_model_lc[1][-1]
            blue_latest_mager = blue_model_lc[2][-1]
        else:
            blue_latest_phase = blue_raw_lc[-1]['phase']
            blue_latest_magvl = blue_raw_lc[-1]['magpsf']
            blue_latest_mager = blue_raw_lc[-1]['sigmapsf']

        if len(red_model_lc) > 0:
            red_latest_phase = red_model_lc[0][-1]
            red_latest_magvl = red_model_lc[1][-1]
            red_latest_mager = red_model_lc[2][-1]
        else:
            red_latest_phase = red_raw_lc[-1]['phase']
            red_latest_magvl = red_raw_lc[-1]['magpsf']
            red_latest_mager = red_raw_lc[-1]['sigmapsf']


        # predefine colour variables to check if colour measurements have been made later
        blue_minus_red_val = ''
        blue_minus_red_err = ''
        
        # if the latest phase is similar in both filters perform the colour measurement immediately
        if -0.125<= (blue_latest_phase - red_latest_phase) <= 0.125:
            blue_minus_red_val = blue_latest_magvl - red_latest_magvl
            blue_minus_red_err = ( (blue_latest_mager**2) + (red_latest_mager**2) )**0.5
        
       # else if the blue filter phase is much later than the red filter phase
       # and blue filter has a modelled light curve
       # loop backwards through blue filter until a matching phase is found
        elif (blue_latest_phase - red_latest_phase) > 0.125 and len(blue_model_lc) > 0:

            for bluephase in reversed(blue_model_lc[0]):
                if (abs(bluephase - red_latest_phase)) <= 0.125:
                    blueidx = blue_model_lc[0].index(bluephase)
                    bluemag = blue_model_lc[1][blueidx]
                    blueerr = blue_model_lc[2][blueidx]
                    blue_minus_red_val = bluemag - red_latest_magvl
                    blue_minus_red_err = ( (blueerr**2) + (red_latest_mager**2) )**0.5
                    break
        
        # else if the red filter phase is much later than the blue filter phase
        # and red filter has a modelled light curve
        # loop backwards through red filter until a matching phase is found
        elif (blue_latest_phase - red_latest_phase) < -0.125 and len(red_model_lc) > 0:

            for redphase in reversed(red_model_lc[0]):
                if (abs(redphase - blue_latest_phase)) <= 0.125:
                    redidx = red_model_lc[0].index(redphase)
                    redmag = red_model_lc[1][redidx]
                    rederr = red_model_lc[2][redidx]
                    blue_minus_red_val = blue_latest_magvl - redmag
                    blue_minus_red_err = ( (blue_latest_mager**2) + (rederr**2) )**0.5
                    break
        
        # if no colour measurement was made then the blue and red filters never allign
        if str(blue_minus_red_val) == '':
            blue_minus_red_val = 'unknown'
            blue_minus_red_err = 'unknown'


    return blue_minus_red_val, blue_minus_red_err



def formatTNSinfo(tnsInfo):

    if 'type' in tnsInfo:
        objtype = tnsInfo['type']
    else:
        objtype = 'Unclassified'
    if 'z' in tnsInfo:
        objz = tnsInfo['z']
    else:
        objz = ''

    tnsdict = {
        "iauname"   : tnsInfo['tns_prefix'] + ' ' + tnsInfo['tns_name'],
        "spectype"  : objtype,
        "redshift"  : objz,
        "discsource": tnsInfo['source_group'],
        "discgroup" : tnsInfo['sender'],
        "discname"  : tnsInfo['disc_int_name'],
        "discdate"  : tnsInfo['disc_date'] + ' UTC',
        "urlname"   : tnsInfo['name'],
    }

    return tnsdict



def coincidesMajorMody(objectData, MOCs):

    in_major_body_dict={}
    # check if the object is inside the galactic plane and flag it
    c_icrs = SkyCoord(ra=objectData['ramean'], dec=objectData['decmean'], unit="deg", frame='icrs')
    if -12.5 < c_icrs.galactic.b.value < +12.5:
        in_major_body_dict['Galactic Plane'] = 'Y'
    else:
        in_major_body_dict['Galactic Plane'] = 'N'
    
    # next check if object is inside any of the major extragalactic bodies
    for MOCname, MOCarea in MOCs.items():

        lon = Angle(np.array([objectData['ramean']]), unit=u.deg)
        lat = Angle(np.array([objectData['decmean']]), unit=u.deg)
        inarea = MOCarea.contains_lonlat(lon=lon, lat=lat)[0]

        if inarea == True:
            in_major_body_dict[MOCname] = 'Y'
        else:
            in_major_body_dict[MOCname] = 'N'

    return in_major_body_dict
