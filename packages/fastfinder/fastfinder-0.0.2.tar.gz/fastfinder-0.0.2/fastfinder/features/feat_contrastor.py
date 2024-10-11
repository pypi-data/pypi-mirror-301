import fastfinder.thresholds as thold
import numpy as np

def contrastFeatureThresholds(objectset, logger):

     # extract features from the objects in the list of objects
    for object in objectset:

        # list the model singleband lightcurves
        object_lc_features = object['lightcurve']['features']

        # iterate through all the features computed and compile a list of comparisons for the fastfinder thresholds defined in thresholds.py
        fast_risers = []
        peak_mag_resembles = []
        fast_faders = []
        peak_mags_maglsit = []
        peak_mags_errlsit = []
        major_Bodies = []
        for lc_filter, lc_features in object_lc_features.items():

            # check the individual filter features first
            if lc_filter in ['lss-u','lsst-g','lsst-r','lsst-i','lsst-z','lsst-y']:
                if len(lc_features) > 0:

                    # check the absolute mag ranges first
                    if lc_features['absolute_peak_mag_val'] != 'unknown':

                        # create lists covering the range of mag values for the object and thresholds
                        peak_mags_maglsit.append(lc_features['absolute_peak_mag_val'])
                        peak_mags_errlsit.append(lc_features['absolute_peak_mag_err'])
                        object_peak_range = np.round(np.arange(round(lc_features['absolute_peak_mag_val'] - 0.67*lc_features['absolute_peak_mag_err'], 1), round(lc_features['absolute_peak_mag_val'] + 0.67*lc_features['absolute_peak_mag_err']+0.1, 1), 0.1).tolist(), 1).tolist()
                        slsn_mag_range = np.round(np.arange(thold.slsn_mag_lim_max, thold.slsn_mag_lim_min+0.1, 0.1).tolist(), 1).tolist()
                        sn_mag_range = np.round(np.arange(thold.sn_mag_lim_max, thold.sn_mag_lim_min+0.1, 0.1).tolist(), 1).tolist()
                        sbsn_mag_range = np.round(np.arange(thold.sbsn_mag_lim_max, thold.sbsn_mag_lim_min+0.1, 0.1).tolist(), 1).tolist()
                        gap_mag_range = np.round(np.arange(thold.gap_mag_lim_max, thold.gap_mag_lim_min+0.1, 0.1).tolist(), 1).tolist()
                        nov_mag_range = np.round(np.arange(thold.nov_mag_lim_max, thold.nov_mag_lim_min+0.1, 0.1).tolist(), 1).tolist()

                        #check if any of the threshold lists overlap the object
                        slsn_overlap = np.arange(max(object_peak_range[0], slsn_mag_range[0]), min(object_peak_range[-1], slsn_mag_range[-1])+0.1, 0.1).tolist()
                        sn_overlap = np.arange(max(object_peak_range[0], sn_mag_range[0]), min(object_peak_range[-1], sn_mag_range[-1])+0.1, 0.1).tolist()
                        sbsn_overlap = np.arange(max(object_peak_range[0], sbsn_mag_range[0]), min(object_peak_range[-1], sbsn_mag_range[-1])+0.1, 0.1).tolist()
                        gap_overlap = np.arange(max(object_peak_range[0], gap_mag_range[0]), min(object_peak_range[-1], gap_mag_range[-1])+0.1, 0.1).tolist()
                        nov_overlap = np.arange(max(object_peak_range[0], nov_mag_range[0]), min(object_peak_range[-1], nov_mag_range[-1])+0.1, 0.1).tolist()

                        # if an overlap exists write that transient class to the resembles list
                        if len(slsn_overlap) > 0:
                            peak_mag_resembles.append('SLSN')
                        if len(sn_overlap) > 0:
                            peak_mag_resembles.append('SN')
                        if len(sbsn_overlap) > 0:
                            peak_mag_resembles.append('Faint-SN')
                        if len(gap_overlap) > 0:
                            peak_mag_resembles.append('Gap')
                        if len(nov_overlap) > 0:
                            peak_mag_resembles.append('Nova')
                    

                    # check the incline rate next
                    if lc_features['overall_incline_rate_val'] != 'unknown':  
                        # if the object incline rate is greater than threshold limit then append "Yes" to the fast risers list
                        # else append "No" to the fast risers list
                        rate = lc_features['overall_incline_rate_val']
                        error = lc_features['overall_incline_rate_err']
                        if rate >= thold.incline_rate and rate/error >= thold.significance:
                            fast_risers.append('F')
                        elif rate-error <= 0.0:
                            fast_risers.append('S')
                        else:
                            fast_risers.append('N')
                    

                    # check the decline rate next
                    if lc_features['overall_decline_rate_val'] != 'unknown':  
                        # if the object decline rate is greater than threshold limit then append "Yes" to the fast faders list
                        # else append "No" to the fast faders list
                        rate = lc_features['overall_decline_rate_val']
                        error = lc_features['overall_decline_rate_err']
                        if rate >= thold.decline_rate and rate/error >= thold.significance:
                            fast_faders.append('F')
                        elif rate-error <= 0.0:
                            fast_faders.append('S')
                        else:
                            fast_faders.append('N')

            # check if the object lies within any of the major bodies
            elif lc_filter == 'in-major-body':
                for Bodyname, flag in lc_features.items():
                    if flag == 'Y':
                        major_Bodies.append(Bodyname)
            
        # Add major bodies to classification description
        if len(major_Bodies) > 0:
            major_Bodies_str = '' + ', '.join(major_Bodies) + ''
            if 'Plane' in major_Bodies_str:
                filler_word = "the "
            else:
                filler_word = ""
            object['explanation'] = f"The object lies within {filler_word}{major_Bodies_str}. "
        else:
            object['explanation'] = ""

        
        # remove duplicates from lists
        fast_risers_lst = list(dict.fromkeys(fast_risers))
        fast_faders_lst = list(dict.fromkeys(fast_faders))
        peak_mag_resembles_lst = list(dict.fromkeys(peak_mag_resembles))

        # Decision tree logic to classify the transient
        if 'F' in fast_risers_lst and 'F' in fast_faders_lst:
            object['classification'] = 'FAST'
            object['explanation'] = object['explanation'] + "The lightcurve is fast rising and fast fading in one or more filters."
        elif 'F' in fast_risers_lst:
            object['classification'] = 'FAST'
            object['explanation'] = object['explanation'] + "The lightcurve is fast rising in one or more filters."
        elif 'F' in fast_faders_lst:
            object['classification'] = 'FAST'
            object['explanation'] = object['explanation'] + "The lightcurve is fast fading in one or more filters."
        elif 'N' in fast_risers_lst or 'N' in fast_faders_lst:
            object['classification'] = 'SN'
            object['explanation'] = object['explanation'] + "The lightcurve evolution resembles that of a supernova."
        else:
            object['classification'] = 'SLOW'
            object['explanation'] = object['explanation'] + "The lightcurve has no significant evolution."
        
        if len(peak_mag_resembles_lst) > 0:
            # identify the brightest peak mag
            brightest_mag_val = min(peak_mags_maglsit)
            brightest_mag_idx = peak_mags_maglsit.index(brightest_mag_val)
            brightest_mag_err = peak_mags_errlsit[brightest_mag_idx]

            peak_mag_resembles_str = '"' + ', '.join(peak_mag_resembles_lst) + '"'
            object['explanation'] = object['explanation'] + f' The predicted range in peak absolute magnitude (M = {round(brightest_mag_val,2)} +/- {round(brightest_mag_err,2)}) lies within the {peak_mag_resembles_str} regime(s).'

        # if the polynomial fit implies features that are not directly measured from the data
        if object['objectData']['isinferred'] == 'Y' and  object['classification'] == 'FAST' and len(peak_mag_resembles_lst) > 0:
            object['classification'] =  object['classification'] + ' (I)'
            object['explanation'] = object['explanation'] + ' The fast nature and peak brightness have been inferred from the fitted models.'
        elif object['objectData']['isinferred'] == 'Y' and  object['classification'] == 'FAST':
            object['classification'] =  object['classification'] + ' (I)'
            object['explanation'] = object['explanation'] + ' The fast nature has been inferred from the fitted models.'
        elif object['objectData']['isinferred'] == 'Y' and  object['classification'] == 'SN':
            object['classification'] =  object['classification'] + ' (I)'
            object['explanation'] = object['explanation'] + ' The supernova-like nature has been inferred from the fitted models.'
        
        # if a colour feature is available add to the description
        if object['lightcurve']['features']['colours']['latest_g_minus_r_val'] != 'unknown':
            colval = round(object['lightcurve']['features']['colours']['latest_g_minus_r_val'],2)
            colerr = round(object['lightcurve']['features']['colours']['latest_g_minus_r_err'],2)
            object['explanation'] = object['explanation'] + f' The latest colour prediction is g-r = {colval} +/- {colerr}.'
            
            if 'visualextinction' in object['objectData'] and object['objectData']['visualextinction'] > thold.lots_of_dust:
                dustval = round(object['objectData']['visualextinction'], 2)
                object['explanation'] = object['explanation'] + f' There is considerable dust reddening (Av = {dustval}) along the line of sight to the transient.'
        
        object['classdict'] = object_lc_features
                    
    return objectset
