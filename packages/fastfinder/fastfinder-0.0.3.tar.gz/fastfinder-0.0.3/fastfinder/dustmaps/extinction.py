import os
import astropy.units as units
from astropy.coordinates import SkyCoord
from dustmaps.config import config

# Dustmap for Schlafly & Finkbeiner & Davis (SFD) 1998
import dustmaps.sfd


def dustLightCurves(objectset, logger, dustmap_location=None):

    # check if SFD DustMaps have already been downloaded
    if dustmap_location and os.path.exists(dustmap_location+"/sfd/"):
        config["data_dir"] = dustmap_location
    else:
        current_path = os.path.dirname(os.path.abspath(__file__))
        maps_exist = os.path.exists(current_path+"/SkyMaps/sfd/")
        if not maps_exist:
            logger.info(f"Downloading SFD 1998 Dustmap. This is a one time download that occurs on a fresh install of Fastfinder.")
            dustmaps.sfd.fetch()
            logger.info(f"Download complete!")
        # setting the extraction query for the SFD Dustmaps
        config["data_dir"] = f"{current_path}/SkyMaps/"
    
    extinction_sky_map = dustmaps.sfd.SFDQuery()

    # iterate through each object in the dataset
    for object in objectset:

        # extract the mean RA and DEC for the object position
        obj_ra = object['objectData']['ramean']
        obj_dec = object['objectData']['decmean']

        # retrieve the E(B-V) value in the line-of-sight of the object from the SFD dustmap
        coords = SkyCoord(obj_ra*units.deg, obj_dec*units.deg, frame="icrs")
        ebv = extinction_sky_map(coords)

        # converting to an E(B-V) value for the SF 2011 dustmap
        # to be used infeature explanations later
        SF11_ebv =  0.86 * ebv
        SF11_Av = 3.1 * SF11_ebv
        object['objectData']['visualextinction'] = SF11_Av

        # converting E(B-V) to individual passband extinctions 
        # coefficients for conversion taken from Table 6: "F99 Reddening in Different Bandpasses" of Schlafly & Finkbeiner (2011) using RV = 3.1
        lsst_u_extinct = round(ebv * 4.145,15)
        lsst_g_extinct = round(ebv * 3.237,15)
        lsst_r_extinct = round(ebv * 2.273,15)
        lsst_i_extinct = round(ebv * 1.684,15)
        lsst_z_extinct = round(ebv * 1.323,15)
        lsst_y_extinct = round(ebv * 1.088,15)
        ps1_g_extinct = round(ebv * 3.172,15)
        ps1_r_extinct = round(ebv * 2.271,15)
        ps1_i_extinct = round(ebv * 1.682,15)
        ps1_w_extinct = round(ebv * 2.341,15)
        atlas_c_extinct = round( (0.49 * ps1_g_extinct) + (0.51 * ps1_r_extinct),15)
        atlas_o_extinct = round( (0.55 * ps1_r_extinct) + (0.45 * ps1_i_extinct),15)
        
        # iterate through the different filter singleband lightcurves
        for filter, lightcurve in object['lightcurve']['raw_singlebands'].items():
            
            # check if the singleband lightcurve has any data
            if len(lightcurve) > 0:

                # loop through each datapoint and subtract the dust extinction
                for datapoint in lightcurve:
                    if filter == 'lsst-u':
                        dustmag = datapoint['magpsf'] - lsst_u_extinct
                    elif filter == 'lsst-g':
                        dustmag = datapoint['magpsf'] - lsst_g_extinct
                    elif filter == 'lsst-r':
                        dustmag = datapoint['magpsf'] - lsst_r_extinct
                    elif filter == 'lsst-i':
                        dustmag = datapoint['magpsf'] - lsst_i_extinct
                    elif filter == 'lsst-z':
                        dustmag = datapoint['magpsf'] - lsst_z_extinct
                    elif filter == 'lsst-y':
                        dustmag = datapoint['magpsf'] - lsst_y_extinct
                    datapoint['magpsf'] = dustmag
        
    return objectset
