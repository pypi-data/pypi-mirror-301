import fastfinder.templates.loader as ftl
import fastfinder.features.lc_modeller as fflcm
import fastfinder.features.lc_extractor as fflce
import fastfinder.features.feat_contrastor as fffc
import fastfinder.features.plotter as fffp
import fastfinder.debug.lc_model_plotter as fdlcmp


def controller(mode, objectset, logger, debug):
    
    # load in the fast finder template datastores
    templates = ftl.loadTemplates(logger)

    # create singleband lightcurve models for the templates and objects in the list of objects
    objectset, templates = fflcm.modelLightCurves(objectset, templates, logger)

    # if debug mode is enabled plot the model lightcurves against the real data lightcurves  
    #if debug == 1:
    #    fdlcmp.setupModelLightCurves(objectset, [], logger)
    
    # extract the brief lightcurve features for objects in the alert stream 
    # and compare to fastfinder thresholds for annotations
    if mode == 'STREAM':
        objectset = fflce.fastFeatureExtractor(objectset, logger)
        objectset = fffc.contrastFeatureThresholds(objectset, logger)
    
    if mode == 'OBJECT':
        objectset = fflce.fastFeatureExtractor(objectset, logger)
        objectset = fffc.contrastFeatureThresholds(objectset, logger)
    
    # plot the lightcurve models against the measured data
    # these plots will be sent into the Slack and useful for discussions
    # plots will be only for FAST classified objects or if Fastfinder was ran in OBJECT mode
    fffp.setupModelLightCurves(mode, objectset, logger)

    return objectset