import numpy as np
import math as m
#try:
import fastfinder.dustmaps.extinction as dust
#except:
#    pass
from astropy.time import Time
from sklearn.metrics import r2_score
from scipy.optimize import minimize
from scipy.optimize import curve_fit
from scipy.optimize import OptimizeWarning
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=OptimizeWarning)


def modelLightCurves(objectset, templates, logger, dustLightCurves=True, dustmap_location=None):

    # split the multiband lightcurves of the objects in the list of objects and templates in template datastore into singleband lightcurves
    objectset, templates = splitLightCurves(objectset, templates, logger)

    # convert the non-detections into pseudo detections to be used in model fitting later
    objectset = fudgeLightCurves(objectset, logger)

    # for the list of objects, stack detections that occur on the same night in the singleband lightcurves
    # additional filter step to remove objects that who individual filters are made up of singletons after stacking
    objectset = stackLightCurves(objectset, logger)
    obj_name_str = ''
    for object in reversed(objectset):
        len_u_lc = len(object['lightcurve']['raw_singlebands']['lsst-u'])
        len_g_lc = len(object['lightcurve']['raw_singlebands']['lsst-g'])
        len_r_lc = len(object['lightcurve']['raw_singlebands']['lsst-r'])
        len_i_lc = len(object['lightcurve']['raw_singlebands']['lsst-i'])
        len_z_lc = len(object['lightcurve']['raw_singlebands']['lsst-z'])
        len_y_lc = len(object['lightcurve']['raw_singlebands']['lsst-y'])
        if len_u_lc < 2 and len_g_lc < 2 and len_r_lc < 2 and len_i_lc < 2 and len_z_lc < 2 and len_y_lc < 2:
            obj_name_str += object['objectId'] +' (<2dpt-after-stack), '
            objectset.remove(object)
            continue
    if len(obj_name_str) != 0:
        logger.info(f"{obj_name_str} - flagged for additional dumping!")
    if len(objectset) == 0:
        logger.warning("All objects were dumped! Cannot proceed with Fastfinder analysis.")
        exit()
    
    # Correct each singleband lightcurve for galactic dust extinction
    if dustLightCurves:
        objectset = dust.dustLightCurves(objectset, logger, dustmap_location)

    # next preoduce polynomial fitted models to the singleband lightcurves
    # templates exist already modelled so need to produce models for only the ingested objects
    for object in objectset:

        # default inferred fit to "N"
        object['objectData']['isinferred'] = 'N'
        
        # iterate through the different singleband lightcurves
        for filter in object['lightcurve']['raw_singlebands']:

            # separate out the lightcurve into xy coords to use in lightcurve model creation
            singleband_lc = object['lightcurve']['raw_singlebands'][filter]
            xData = [epoch['phase'] for epoch in singleband_lc]
            yData = [epoch['magpsf'] for epoch in singleband_lc]
            yDataErr = [epoch['sigmapsf'] for epoch in singleband_lc]

            # if there is more than one epoch in the filter then create a lightcure model for the filter
            # should always be the case as raw singleband lightcurves are not created for filters with only one epoch
            if len(xData) > 1:

                xModel, yModel, yModelErr, is_inferred = curveFitting(xData, yData, yDataErr, logger, object['objectId']+'-'+filter)
                object['lightcurve']['model_singlebands'][filter] = [xModel,yModel,yModelErr]
            
                # check if any of the fits are inferred
                if is_inferred:
                    object['objectData']['isinferred'] = 'Y'

    return objectset, templates



def splitLightCurves(objectset, templates, logger):

    # Deal with the objects first
    for object in objectset:

        # extract the entire multiband lightcurve
        object_lc = object['lightcurve']['raw_multibands']

        # append a global phase value to the multiband lightcurve epochs
        # phase variable w.r.t to first detection in any filter
        first_det = [epoch for epoch in object_lc if 'candid' in epoch][0]
        for epoch in object_lc:
            epoch['phase'] = round(epoch['jd'] - first_det['jd'], 3)
        
        # separate the multiband lightcurve into its singleband lighcures
        # note: need to update this for LSST once LSST data is available
        object_lc_u = []
        object_lc_g = []
        object_lc_r = []
        object_lc_i = []
        object_lc_z = []
        object_lc_y = []
        for epoch in object_lc:
            if epoch['fid'] == 1:
                object_lc_g.append(epoch)
            elif epoch['fid'] == 2:
                object_lc_r.append(epoch)

        # finally add the separated singleband lightcurves to the lightcurve directory of the object
        object['lightcurve']['raw_singlebands']['lsst-u'] = object_lc_u
        object['lightcurve']['features']['lsst-u'] = {}
        object['lightcurve']['raw_singlebands']['lsst-g'] = object_lc_g
        object['lightcurve']['features']['lsst-g'] = {}
        object['lightcurve']['raw_singlebands']['lsst-r'] = object_lc_r
        object['lightcurve']['features']['lsst-r'] = {}
        object['lightcurve']['raw_singlebands']['lsst-i'] = object_lc_i
        object['lightcurve']['features']['lsst-i'] = {}
        object['lightcurve']['raw_singlebands']['lsst-z'] = object_lc_z
        object['lightcurve']['features']['lsst-z'] = {}
        object['lightcurve']['raw_singlebands']['lsst-y'] = object_lc_y
        object['lightcurve']['features']['lsst-y'] = {}


    # Deal with templates in the template datastore next
    for spec_type in templates:

        # iterate through each of the templates of the different spectral types
        for template in templates[spec_type]:

            # extract the entire mutliband lightcurve
            template_lc = [epoch for epoch in templates[spec_type][template]['lightcurve']['candidates']]

            # separate the multiband lightcurve into its separate band lighcures
            template_lc_u = []
            template_lc_g = []
            template_lc_r = []
            template_lc_i = []
            template_lc_z = []
            template_lc_y = []
            template_lc_w = []
            template_lc_c = []
            template_lc_o = []
            for epoch in template_lc:
                if epoch['lsst-u'] != '':
                    template_lc_u.append({'phase':epoch['phase'], 'magpsf':epoch['lsst-u']})
                if epoch['lsst-g'] != '':
                    template_lc_g.append({'phase':epoch['phase'], 'magpsf':epoch['lsst-g']})
                if epoch['lsst-r'] != '':
                    template_lc_r.append({'phase':epoch['phase'], 'magpsf':epoch['lsst-r']})
                if epoch['lsst-i'] != '':
                    template_lc_i.append({'phase':epoch['phase'], 'magpsf':epoch['lsst-i']})
                if epoch['lsst-z'] != '':
                    template_lc_z.append({'phase':epoch['phase'], 'magpsf':epoch['lsst-z']})
                if epoch['lsst-y'] != '':
                    template_lc_y.append({'phase':epoch['phase'], 'magpsf':epoch['lsst-y']})
                if epoch['ps-w'] != '':
                    template_lc_w.append({'phase':epoch['phase'], 'magpsf':epoch['ps-w']})
                if epoch['atlas-c'] != '':
                    template_lc_c.append({'phase':epoch['phase'], 'magpsf':epoch['atlas-c']})
                if epoch['atlas-o'] != '':
                    template_lc_o.append({'phase':epoch['phase'], 'magpsf':epoch['atlas-o']})

            # finally add the separated singleband lightcurves to the lightcurve directory of the template in the template datastore
            if len(template_lc_u) > 0:
                singleband_lc = [epoch for epoch in template_lc_u]
                xData = [epoch['phase'] for epoch in singleband_lc]
                yData = [epoch['magpsf'] for epoch in singleband_lc]
                templates[spec_type][template]['lightcurve']['model_singlebands']['lsst-u'] = [xData,yData]
                templates[spec_type][template]['lightcurve']['features']['lsst-u'] = {}
            if len(template_lc_g) > 0:
                singleband_lc = [epoch for epoch in template_lc_g]
                xData = [epoch['phase'] for epoch in singleband_lc]
                yData = [epoch['magpsf'] for epoch in singleband_lc]
                templates[spec_type][template]['lightcurve']['model_singlebands']['lsst-g'] = [xData,yData]
                templates[spec_type][template]['lightcurve']['features']['lsst-g'] = {}
            if len(template_lc_r) > 0:
                singleband_lc = [epoch for epoch in template_lc_r]
                xData = [epoch['phase'] for epoch in singleband_lc]
                yData = [epoch['magpsf'] for epoch in singleband_lc]
                templates[spec_type][template]['lightcurve']['model_singlebands']['lsst-r'] = [xData,yData]
                templates[spec_type][template]['lightcurve']['features']['lsst-r'] = {}
            if len(template_lc_i) > 0:
                singleband_lc = [epoch for epoch in template_lc_i]
                xData = [epoch['phase'] for epoch in singleband_lc]
                yData = [epoch['magpsf'] for epoch in singleband_lc]
                templates[spec_type][template]['lightcurve']['model_singlebands']['lsst-i'] = [xData,yData]
                templates[spec_type][template]['lightcurve']['features']['lsst-i'] = {}
            if len(template_lc_z) > 0:
                singleband_lc = [epoch for epoch in template_lc_z]
                xData = [epoch['phase'] for epoch in singleband_lc]
                yData = [epoch['magpsf'] for epoch in singleband_lc]
                templates[spec_type][template]['lightcurve']['model_singlebands']['lsst-z'] = [xData,yData]
                templates[spec_type][template]['lightcurve']['features']['lsst-z'] = {}
            if len(template_lc_y) > 0:
                singleband_lc = [epoch for epoch in template_lc_y]
                xData = [epoch['phase'] for epoch in singleband_lc]
                yData = [epoch['magpsf'] for epoch in singleband_lc]
                templates[spec_type][template]['lightcurve']['model_singlebands']['lsst-y'] = [xData,yData]
                templates[spec_type][template]['lightcurve']['features']['lsst-y'] = {}
            if len(template_lc_w) > 0:
                singleband_lc = [epoch for epoch in template_lc_w]
                xData = [epoch['phase'] for epoch in singleband_lc]
                yData = [epoch['magpsf'] for epoch in singleband_lc]
                templates[spec_type][template]['lightcurve']['model_singlebands']['ps-w'] = [xData,yData]
                templates[spec_type][template]['lightcurve']['features']['ps-w'] = {}
            if len(template_lc_c) > 0:
                singleband_lc = [epoch for epoch in template_lc_c]
                xData = [epoch['phase'] for epoch in singleband_lc]
                yData = [epoch['magpsf'] for epoch in singleband_lc]
                templates[spec_type][template]['lightcurve']['model_singlebands']['atlas-c'] = [xData,yData]
                templates[spec_type][template]['lightcurve']['features']['atlas-c'] = {}
            if len(template_lc_o) > 0:
                singleband_lc = [epoch for epoch in template_lc_o]
                xData = [epoch['phase'] for epoch in singleband_lc]
                yData = [epoch['magpsf'] for epoch in singleband_lc]
                templates[spec_type][template]['lightcurve']['model_singlebands']['atlas-o'] = [xData,yData]
                templates[spec_type][template]['lightcurve']['features']['atlas-o'] = {}

    return objectset, templates




def fudgeLightCurves(objectset, logger):

    # loop through each singleband lightcurve and turn the non detections into pseudo detections
    for object in objectset:

        # iterate through the different filter singleband lightcurves
        for filter in object['lightcurve']['raw_singlebands']:

            # grab the single band lightcurve for the filter in iteration
            singleband_lc = object['lightcurve']['raw_singlebands'][filter]

            if len(singleband_lc) > 0:
                alt_epochs = []
                for epoch in singleband_lc:
                    # generate the metadata for the pseudo detection
                    # round the MJD to 3 d.p. for stacking and modelling later
                    if 'candid' not in epoch:
                        synth_epoch = {
                            'candid': 'nondet',
                            'jd': epoch['jd'],
                            'ra': round(object['objectData']['ramean'],7),
                            'dec': round(object['objectData']['decmean'],7),
                            'fid': epoch['fid'], 
                            'nid': None,
                            'magpsf': epoch['magpsf'],
                            'sigmapsf': np.nan,
                            'magnr': None,
                            'sigmagnr': None,
                            'magzpsci': None,
                            'isdiffpos': 't',
                            'ssdistnr': None,
                            'ssnamenr': None,
                            'drb': None,
                            'mjd': round(epoch['mjd'],3),
                            'since_now': epoch['since_now'],
                            'utc': Time(epoch['jd'], format='jd').to_value('iso'),
                            'phase': epoch['phase']
                            }
                        epoch = synth_epoch
                    else:
                        epoch['candid'] = 'det'
                        epoch['mjd'] = round(epoch['mjd'],3)
                    alt_epochs.append(epoch)
                object['lightcurve']['raw_singlebands'][filter] = alt_epochs

    return objectset




def stackLightCurves(objectset, logger):

    # define the MJD binning size as 0.125 days (3 hours)
    binesize_thold = 0.125

    # iterate through each object in the dataset
    for object in objectset:
        
        # iterate through the different filter singleband lightcurves
        for filter in object['lightcurve']['raw_singlebands']:

            # grab the single band lightcurve for the filter in iteration
            singleband_lc = object['lightcurve']['raw_singlebands'][filter]

            # if there is more than one epoch in the lightcurve perform the binning sequence
            stacked_bins = [] 
            if len(singleband_lc) > 1:
                
                # list out all the mjds in the lightcurve and define bin edges
                all_mjds_lsit = [epoch['mjd'] for epoch in singleband_lc]               
                for base_mjd in list(all_mjds_lsit):
                    for check_mjd in list(all_mjds_lsit):
                        if 0 < check_mjd - base_mjd < binesize_thold:
                            all_mjds_lsit.remove(check_mjd)
                
                # bin the detections keyed on the binning mjds
                binned_detections = {}
                for mjd in all_mjds_lsit:
                    binned_mjd_dets = []
                    for detection in singleband_lc:
                        if 0 <= detection['mjd'] - mjd < 0.125:
                            binned_mjd_dets.append(detection)
                    binned_detections[mjd] = binned_mjd_dets
                
                # get the list of detections for each bin and flux stack them
                for bin_mjd, bin_detections in binned_detections.items():

                    nondets_cnt = len([epoch for epoch in bin_detections if epoch['candid']=='nondet'])
                    dets_cnt = len([epoch for epoch in bin_detections if epoch['candid']=='det'])

                    # if bin is made up of only non-detections take the deepest non-detection for the bin stack
                    if nondets_cnt > 0 and dets_cnt == 0:

                        deepNonDet = max(bin_detections, key=lambda x:x['magpsf'])
                        
                        stack_candid      = 'stacknondet'
                        stacked_jd        = deepNonDet['jd']
                        stacked_ra        = deepNonDet['ra']
                        stacked_dec       = deepNonDet['dec']
                        stacked_fid       = deepNonDet['fid']
                        stacked_nid       = None
                        stacked_magpsf    = deepNonDet['magpsf']
                        stacked_sigmapsf  = deepNonDet['sigmapsf']
                        stacked_magnr     = None
                        stacked_sigmagnr  = None
                        stacked_magzpsci  = None
                        stacked_isdiffpos = 't'
                        stacked_ssdistnr  = None
                        stacked_ssnamenr  = None
                        stacked_drb       = None
                        stacked_mjd       = deepNonDet['mjd']
                        stacked_since_now = deepNonDet['since_now']
                        stacked_utc       = deepNonDet['utc']
                        stacked_phase     = deepNonDet['phase']
                    
                    # else if bin contains any detection, then take average of those detections for the bin stack
                    elif dets_cnt > 0:

                        bin_detections_dets = [epoch for epoch in bin_detections if epoch['candid']=='det']

                        stacked_bin = {}
                        sum_weighted_flux = 0
                        sum_weights = 0
                        for det in bin_detections_dets:
                            # turn magnitudes into microjansky flux for stacking
                            uJy = 10**((det['magpsf'] - 23.9) / -2.5)
                            duJy = uJy * det['sigmapsf']
                            # find the sum of the weighted flux and sum of the weights in the bin
                            weight = 1.0 / (duJy**2)
                            weighted_flux = uJy * weight
                            sum_weighted_flux += weighted_flux
                            sum_weights += weight
                        # find the weighted mean flux
                        mean_flux = sum_weighted_flux / sum_weights
                        # find the the error on the weighted mean flux
                        mean_dlux = (1.0 / sum_weights)**0.5
                        # turn stacked flux back into magnitudes
                        mean_mag = -2.5 * m.log10(mean_flux) + 23.9
                        mean_dmag = mean_dlux/mean_flux

                        stack_candid      = 'stackdet'
                        stacked_jd        = float(sum(key['jd'] for key in bin_detections_dets)) / len(bin_detections_dets)
                        stacked_ra        = round(float(sum(key['ra'] for key in bin_detections_dets)) / len(bin_detections_dets),7)
                        stacked_dec       = round(float(sum(key['dec'] for key in bin_detections_dets)) / len(bin_detections_dets),7)
                        stacked_fid       =   int(sum(key['fid'] for key in bin_detections_dets) / len(bin_detections_dets))
                        stacked_nid       = None
                        stacked_magpsf    = mean_mag
                        stacked_sigmapsf  = mean_dmag
                        stacked_magnr     = None
                        stacked_sigmagnr  = None
                        stacked_magzpsci  = None
                        stacked_isdiffpos = 't'
                        stacked_ssdistnr  = None
                        stacked_ssnamenr  = None
                        stacked_drb       = None
                        stacked_mjd       = round(float(sum(key['mjd'] for key in bin_detections_dets)) / len(bin_detections_dets),3)
                        stacked_since_now = float(sum(key['since_now'] for key in bin_detections_dets)) / len(bin_detections_dets)
                        stacked_utc       = Time(stacked_jd, format='jd').to_value('iso')
                        stacked_phase     = round(float(sum(key['phase'] for key in bin_detections_dets)) / len(bin_detections_dets),3)

        
                    # create a candidate dictonary for the stacked detection
                    stacked_bin = {
                        'candid': stack_candid,
                        'jd': stacked_jd,
                        'ra': stacked_ra,
                        'dec': stacked_dec,
                        'fid': stacked_fid,
                        'nid': stacked_nid,
                        'magpsf': stacked_magpsf,
                        'sigmapsf': stacked_sigmapsf,
                        'magnr': stacked_magnr,
                        'sigmagnr': stacked_sigmagnr,
                        'magzpsci': stacked_magzpsci,
                        'isdiffpos': stacked_isdiffpos,
                        'ssdistnr': stacked_ssdistnr,
                        'ssnamenr': stacked_ssnamenr,
                        'drb': stacked_drb,
                        'mjd': stacked_mjd,
                        'since_now': stacked_since_now,
                        'utc': stacked_utc,
                        'phase': stacked_phase
                    }
                    stacked_bins.append(stacked_bin)

                # reset the singleband lightcurve to the stacked version
                object['lightcurve']['raw_singlebands'][filter] = stacked_bins
            
            # else set the singleband lightcurve to the extracted version without the non detections
            else:
                object['lightcurve']['raw_singlebands'][filter] = singleband_lc

    return objectset



def curveFitting(xData, yData, yDataErr, logger, objectId):

    #print(objectId)

    # if the light curve consists of only three epochs check if the peak lies in the middle of the time range
    # if not then mark the peak as skewed and skip polynomial fitting as an inflated peak will form
    t_min = min(xData)
    t_max = max(xData)
    t_range = t_max - t_min
    
    if len(xData) == 3:
        peak_idx = yData.index(min(yData))
        if peak_idx == 1:
            peak_time = xData[peak_idx]
            t_lower = t_min + 1 * (t_range / 3)
            t_upper = t_max - 1 * (t_range / 3)
            if t_lower < peak_time < t_upper:
                skewed_peak = False
            else:
                skewed_peak = True
        else:
            skewed_peak = False
    else:
        skewed_peak = False
    
    # if there are more than two datapoints to model
    # and if the datpoints aren't skewed attempt lightcurve modelling
    R2score_thold_ploy = 0.975
    R2score_thold_pwr  = 0.995
    R2score_polyfit = 0.0
    R2score_powerlaw = 0.0
    if len(xData) > 2 and not skewed_peak:

        # first check if a powerlaw fit is possible as it is a more restrictive fitting procedure
        peak_idx = yData.index(min(yData))
        yData_postpeak = yData[peak_idx:]
        xData_postpeak = xData[peak_idx:]
        yDataErr_postpeak = yDataErr[peak_idx:] 
        yData_prepeak = yData[:peak_idx]
        xData_prepeak = xData[:peak_idx]
        
        if len(yData_postpeak) > 2 and len(yData_prepeak) < 3:
            
            # remove non-detections from the data
            nondet_idxs = [yDataErr_postpeak.index(dp) for dp in yDataErr_postpeak if np.isnan(dp)]
            for idx in reversed(nondet_idxs):
                xData_postpeak.pop(idx)
                yData_postpeak.pop(idx)
                yDataErr_postpeak.pop(idx)

            R2score_powerlaw, popt_pwr, mjd_offset_pwr = pwrDecayFit(xData_postpeak, yData_postpeak, yDataErr_postpeak, R2score_thold_pwr)
        else:
            R2score_powerlaw = 0.0


        # check if the data has non detections
        nondets = [val for val in yDataErr if np.isnan(val)]
        # always attempt a polynomial fit to the data
        # regardless if a powerlaw fit was attempted
        if len(nondets) > 0:
            R2score_polyfit, popt_poly = polyFitNonDets(xData, yData, yDataErr, R2score_thold_ploy)
        else:
            R2score_polyfit, popt_poly = polyFitDets(xData, yData, yDataErr, R2score_thold_ploy)

        
        # check if if the powerlaw decay fit is accurate enough
        if R2score_powerlaw >= R2score_thold_pwr:
            tfine = np.arange(min(xData_postpeak)+mjd_offset_pwr,max(xData_postpeak)+mjd_offset_pwr+0.001,0.001)
            Xmod = [round(x,3) for x in tfine]
            Ymod = list(powerlaw(Xmod, *popt_pwr))
            Xmod = [phs-mjd_offset_pwr for phs in Xmod]
            Ymoderr = errorModellingDists(tfine, [phs+mjd_offset_pwr for phs in xData_postpeak], yData_postpeak, yDataErr_postpeak, popt_pwr, 'PWR') 
            
            # if there is any data prior to the peak
            # check the peak is significantly brighter than the epoch prior to peak
            # and model the rise component through connect the dots
            yData_peak_err_thold = yDataErr[peak_idx]
            if len(xData_prepeak) > 0 and yData_prepeak[-1] - yData_postpeak[0] > yData_peak_err_thold:
                X_prepeak = []
                Y_prepeak = []
                Yerr_prepeak = []
                X_prepeak.append(xData_prepeak[-1])
                X_prepeak.append(Xmod[0])
                Y_prepeak.append(yData_prepeak[-1])
                Y_prepeak.append(Ymod[0])
                Yerr_prepeak.append(Ymoderr[0])
                Yerr_prepeak.append(Ymoderr[0])
                Xmod_prepeak, Ymod_prepeak, Ymoderr_prepeak = connectTheDots(X_prepeak, Y_prepeak, Yerr_prepeak)
                Xmod_prepeak.pop()
                Ymod_prepeak.pop()
                Ymoderr_prepeak.pop()
                Xmod = Xmod_prepeak + Xmod
                Ymod = Ymod_prepeak + Ymod
                Ymoderr = Ymoderr_prepeak + Ymoderr


        # else check if any of the polynomial fits are accurate enough
        elif R2score_polyfit >= R2score_thold_ploy:
            poly = np.poly1d(popt_poly)
            tfine = np.arange(t_min,t_max+0.001,0.001)
            Xmod = [round(x,3) for x in tfine]
            Ymod = list(poly(Xmod))
            Ymoderr = errorModellingDists(tfine, xData, yData, yDataErr, popt_poly, 'POLY')
         # else abort to the connect the dots procedure
        else:
            Xmod, Ymod, Ymoderr = connectTheDots(xData, yData, yDataErr)
        
    # else if too few datapoints or the datapoints are skewed 
    # connect the datpoints via straight lines instead
    else:    
        Xmod, Ymod, Ymoderr = connectTheDots(xData, yData, yDataErr)
    
    
    # check if the measured peak lies within range of the modelled peak
    meas_peak_val = min(yData)
    meas_peak_idx = yData.index(meas_peak_val)
    meas_peak_err = yDataErr[meas_peak_idx]
    meas_peak_phs = xData[meas_peak_idx]

    modl_peak_val = min(Ymod)
    modl_peak_idx = Ymod.index(modl_peak_val)
    modl_peak_phs = Xmod[modl_peak_idx]

    if (meas_peak_phs - 2*0.125 <= modl_peak_phs <= meas_peak_phs + 2*0.125) and (meas_peak_val - meas_peak_err <= modl_peak_val <= meas_peak_val + meas_peak_err):
        feats_inferred = False
    else:
        feats_inferred = True


    return Xmod, Ymod, Ymoderr, feats_inferred




def polyFitNonDets(xData, yData, yDataErr, R2score_thold):

    # determine the maximum polynomial degree that can be fitted
    # based on the number of detections and the cadence of detections
    deg = 1
    cadence_list = []
    for idx, val in enumerate(xData):
        if idx + 1 < len(xData):
            cadence_list.append(xData[idx+1] - xData[idx])
    max_gap = max(cadence_list)
    min_gap = min(cadence_list)

    if len(xData) < 5:
        deg_thold = 2
    elif max_gap / min_gap <= 2.0:
        deg_thold = len(xData) - 1
    else:
        deg_thold = int(round(len(xData)**0.5,0))
    if deg_thold > 5:
        deg_thold = 5

    # assign a starting value to the error on the non detections
    # the accuracy of the non-detection cannot be better than the accuracy of the most accurate detection
    # and the accuracy of the non-detection cannot be worse than a 3-sigma detection
    min_err = min([val for val in yDataErr if ~np.isnan(val)])
    upplim_err = min_err
    upplim_thold = 0.35
    # find the polynomial that best represents the observed data
    # using a combination of polyfit, chi^2 and R^2 scores
    r2score = 0.0
    r2score_dict = {}
    # R2 score needed in while clause to ostain the best fitting lowest degree polynomial
    while r2score <= R2score_thold and deg <= deg_thold:

        # manually perform a chi^2 check on the polynomial fit
        def chi2fit(coeffs):
            poly = np.poly1d(coeffs)
            chi2 = 0
            for i in range(len(xData)):
                if ~np.isnan(yDataErr[i]):
                    chi2 += (yData[i] - poly(xData[i]))**2 / yDataErr[i]**2
                else:
                    if poly(xData[i]) > yData[i]:
                        pass
                    else:
                        chi2 += (yData[i] - poly(xData[i]))**2 / upplim_err**2
            return chi2
        
        # define starting values on the polynomial coefficients to begin optimization
        # length of x0 = to number of coefficients for polyfit = degree + 1
        c0 = np.ones(deg+1)*10
        # optimize the polynomial fit based on current upper limit errors
        popts = minimize(chi2fit, c0)
        
        # calculate weights for the data after penalizing the upper limits
        yDataErrAllDps = [upplim_err if np.isnan(x) else x for x in yDataErr]
        weights = [1/(err) for err in yDataErrAllDps]

        # calculate the R^2 score of the polynomial fit to the weighted lightcurve with optimized coefficients
        r2score = r2_score(yData, np.polyval(popts.x, xData), sample_weight=weights)
        r2score_dict[r2score] = popts.x

        # if a good fit was not obtained with current polynomial order and the upper limit penalizer threshold has been reached
        # increase degree of polynomial order and try again
        # until max polynomial order is reached as determined by while loop
        upplim_err += 0.01
        if upplim_err > upplim_thold:
            upplim_err = min_err
            deg += 1
    
    # define final polynomial model after optimization
    # based on which set of coefficients got the best R2 score
    max_R2score = max(r2score_dict.keys())
    popt = r2score_dict[max_R2score]

    return max_R2score, popt



def polyFitDets(xData, yData, yDataErr, R2score_thold):

    # determine the maximum polynomial degree that can be fitted
    # based on the number of detections and the cadence of detections
    deg = 1
    cadence_list = []
    for idx, val in enumerate(xData):
        if idx + 1 < len(xData):
            cadence_list.append(xData[idx+1] - xData[idx])
    max_gap = max(cadence_list)
    min_gap = min(cadence_list)

    if max_gap / min_gap <= 2.0:
        deg_thold = len(xData) - 1
    else:
        deg_thold = int(round(len(xData)**0.5,0))
    if deg_thold > 5:
        deg_thold = 5

    r2score = 0.0
    r2score_dict = {}
    # optimize the polynomial curve fit
    # R2 score needed in while clause to ostain the best fitting lowest degree polynomial
    while r2score <= R2score_thold and deg <= deg_thold:

        # calculate weights for the detections 
        weights = [1/(err) for err in yDataErr]

        # fit an optimized nth degree polynomial to the non lightcurve and obtain the coefficients of the fit
        popts, pcov = np.polyfit(xData, yData, deg, w=weights, cov='unscaled')

        # calculate the R^2 score of the polynomial fit with optimized coefficients
        r2score = r2_score(yData, np.polyval(popts, xData), sample_weight=weights)
        r2score_dict[r2score] = popts

        # if a good fit was not obtained with current polynomial order
        # increase degree of polynomial order and try again
        # until max polynomial order is reached
        deg += 1
    
    # define final polynomial model after optimization
    # based on which set of coefficients got the best R2 score
    max_R2score = max(r2score_dict.keys())
    popt = r2score_dict[max_R2score]

    return max_R2score, popt



def pwrDecayFit(xData, yData, yDataErr, R2score_thold):

    weights = [1/(err) for err in yDataErr]

    r2score = 0.0
    mjd_offset = 0.0
    r2score_dict = {}
    mjd_offset_dict = {}

    # same powerlaw formula being used with changing arbitary scaling, don't need to include check on R2 score in while clause
    while mjd_offset <= 10:

        # add an arbitary phase (mjd) offset to the data
        xData_offset = [xdp+mjd_offset for xdp in xData]

        # try and fit a powerlaw decay to the data and optimize the fit
        try:
            popt, pcov = curve_fit(powerlaw, xData_offset, yData, check_finite=True, sigma=yDataErr, absolute_sigma=True, maxfev=10000)
            # calculate the R2 score for the optimized powerlaw fit
            r2score = r2_score(yData, powerlaw(xData_offset, *popt), sample_weight=weights)
        # if anything goes wrong abort and set default values
        except:
            r2score = 0.0
            popt = [0,0]
        
        r2score_dict[r2score] = popt
        mjd_offset_dict[r2score] = mjd_offset
        mjd_offset += 0.1
    
    # define final polynomial model after optimization
    # based on which set of coefficients got the best R2 score
    max_R2score = max(r2score_dict.keys())
    popt = r2score_dict[max_R2score]
    pmjd_offset = mjd_offset_dict[max_R2score]
    
    return max_R2score, popt, pmjd_offset

# Power-law comparision
def powerlaw(t, k, alpha):
    Ft = k * (t**-alpha)
    return Ft



def connectTheDots(xData, yData, yDataErr):

    Xmod = []
    Ymod = []
    i = 0
    while i+1 < len(xData):
        time = [xData[i], xData[i+1]]
        mag  = [yData[i], yData[i+1]]
        tfine = np.arange(xData[i],xData[i+1],0.001)
        fit_coefficients = np.polyfit(time,mag,1)
        fit_line = fit_coefficients[0]*tfine + fit_coefficients[1]
        Xmod.extend(tfine)
        Ymod.extend(fit_line)
        i+=1
    Xmod.append(xData[-1])
    Ymod.append(yData[-1])

    yDataErr_adj = [err for err in yDataErr if not np.isnan(err)]
    yDataErr_avr = sum(yDataErr_adj) / len(yDataErr_adj)

    Ymoderr = list(np.ones(len(Ymod)) * yDataErr_avr)

    return Xmod, Ymod, Ymoderr



def errorModellingDists(tfine, xData, yData, yDataErr, popt, mode):
    
    y__y_pred_dists = []

    if mode == 'POLY':
        poly = np.poly1d(popt)
        yDataErr_len = len([err for err in yDataErr if not np.isnan(err)])

        for i in range(len(xData)):
            if ~np.isnan(yDataErr[i]):
                dist = (yData[i]-poly(xData[i]))**2 + yDataErr[i]**2
                y__y_pred_dists.append(dist)
    
    if mode == 'PWR':
        yDataErr_len = len([err for err in yDataErr if not np.isnan(err)])
        
        for i in range(len(xData)):
             if ~np.isnan(yDataErr[i]):
                dist = (yData[i]-powerlaw(xData[i], *popt))**2 + yDataErr[i]**2
                y__y_pred_dists.append(dist)
    
    YmodErr = (sum(y__y_pred_dists)**0.5) / yDataErr_len

    return list(np.ones(len(tfine))*YmodErr)
