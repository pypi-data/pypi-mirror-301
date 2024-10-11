import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as mticker

plt.rcParams['font.family']='Times New Roman'
plt.rcParams['figure.figsize']=11.7,7.3
plt.rcParams['figure.autolayout']=True
plt.rcParams['mathtext.fontset']='dejavuserif' 

# plot the raw and modelled lightcurve data for the objects classified as FAST or if Fastfinder is ran in OBJECT mode
def setupModelLightCurves(mode, objectset, logger):

    for object in objectset:
        if mode == 'OBJECT' or 'FAST' in object['classification']:
            plotModelLightCurves(object['objectId'], object['lightcurve']['raw_singlebands'], object['lightcurve']['model_singlebands'], object['classdict'], object['lightcurve']['features']['tns'], object['objectData'], logger)
    return



def plotModelLightCurves(objectId, rawdata, modeldata, classdict, tnsdata, objdata, logger):

    if len(tnsdata) > 0:
        iauname = tnsdata['iauname']
        spectyp = tnsdata['spectype']
    else:
        iauname = 'Unregistered'
        spectyp = 'Unknown'

    if objdata['isinferred'] == 'Y':
        inferred = 'Yes'
    else:
        inferred = 'No'
    
    if str(objdata['z']) != '' and objdata['z'] != 0.0:
        redshift = str(round(objdata['z'],4))
    elif str(objdata['photoZ']) != '' and objdata['photoZ'] != 0.0:
        redshift = str(round(objdata['photoZ'],4)) + " \u00B1 " + str(round(objdata['dphotoZ'],4)) + " (photoZ)"
    else:
        redshift = 'Unknown'
    
    if str(objdata['m-M']) != '' and objdata['m-M'] != 0.0:
        distmod = str(round(objdata['m-M'],2)) + " \u00B1 " + str(round(objdata['dm-M'],2))
    else:
        distmod = 'Unknown'

    
    fig = plt.figure()
    fig.set_tight_layout(False)
    ax1 = fig.add_axes([0.08, 0.15, 0.68, 0.80])
    legend_elements = []

    for filter in modeldata:

        loop_filter = filter
        loop_modeldata = modeldata[filter]
        loop_rawdata = rawdata[filter]
        loop_metadata = classdict[filter]

        if str(loop_metadata['absolute_peak_mag_err']) != 'unknown':
            peak_str =  str(loop_metadata['absolute_peak_mag_val']) + " \u00B1 " +  str(loop_metadata['absolute_peak_mag_err'])
        else:
            peak_str = 'N/A \u00B1 N/A'

        if str(loop_metadata['overall_incline_rate_err']) != 'unknown':
            incline_str = str(loop_metadata['overall_incline_rate_val']) + " \u00B1 " +  str(loop_metadata['overall_incline_rate_err'])
        else:
            incline_str = 'N/A \u00B1 N/A'
        
        if str(loop_metadata['overall_decline_rate_err']) != 'unknown':
            decline_str =  str(loop_metadata['overall_decline_rate_val']) + " \u00B1 " +  str(loop_metadata['overall_decline_rate_err'])
        else:
            decline_str = 'N/A \u00B1 N/A'

        # colours taken from https://github.com/lsst-uk/lasair-lsst/blob/main/webserver/lasair/apps/object/utils.py
        if loop_filter == 'lsst-u':
            markerclolour = "#9900CC"
            markerorder = 16
            xpos = 0.78
            ypos = 0.95
        if loop_filter == 'lsst-g':
            markerclolour = "#3366FF"
            markerorder = 15
            xpos = 0.78
            ypos = 0.80
        if loop_filter == 'lsst-r':
            markerclolour = "#33cc33"
            markerorder = 14
            xpos = 0.78
            ypos = 0.65
        if loop_filter == 'lsst-i':
            markerclolour = "#ffcc00"
            markerorder = 13
            xpos = 0.78
            ypos = 0.50
        if loop_filter == 'lsst-z':
            markerclolour = "#ff0000"
            markerorder = 12
            xpos = 0.78
            ypos = 0.35
        if loop_filter == 'lsst-y':
            markerclolour = "#cc6600"
            markerorder = 11
            xpos = 0.78
            ypos = 0.20

        legend_elements.append(Line2D([0], [0], color=markerclolour, marker='o', markersize=8, linestyle='--', label=f'{loop_filter}'))
        props = dict(boxstyle='round', facecolor=markerclolour, alpha=0.67)
        ax1.text    (xpos, ypos, f'Abs. Mag = {peak_str}\nIncline Rate = {incline_str}\nDecline Rate = {decline_str}', transform=plt.gcf().transFigure, fontsize=14, verticalalignment='top', bbox=props)

        for epoch in loop_rawdata:
            if 'nondet' in epoch['candid']:
                ax1.plot    (epoch['phase'], epoch['magpsf'], marker='o', markersize=8, color=markerclolour, fillstyle='none', zorder=markerorder)
            else:
                ax1.errorbar(epoch['phase'], epoch['magpsf'], epoch['sigmapsf'], marker='o', markersize=8, ls='none', elinewidth=2.5, markeredgewidth=2.5, capsize=0.5, color=markerclolour, zorder=markerorder)

        ax1.plot        (loop_modeldata[0], loop_modeldata[1], linestyle='--', color=markerclolour, alpha=0.67, zorder=markerorder-10)
        ax1.fill_between(loop_modeldata[0], [a_i - b_i for a_i, b_i in zip(loop_modeldata[1], loop_modeldata[2])], [a_i + b_i for a_i, b_i in zip(loop_modeldata[1], loop_modeldata[2])], color=markerclolour, alpha=0.25, zorder=markerorder-10)
    
    
    #legend_elements.append(Line2D([0], [0], color='black', marker='o', linestyle='', markersize=8, label=f'Data'))
    #legend_elements.append(Line2D([0], [0], color='black', marker='', linestyle='--', markersize=8, label=f'Model'))
    ax1.legend(handles=legend_elements, loc='best', prop={'size':14.5}, ncol=2, columnspacing=1, handletextpad=0).set_zorder(0)

    ax1.set_title(f"{objectId}", fontsize=24, pad=10)
    ax1.set_ylabel("Apparent Magnitude + Dust Cor. [AB Mag]", fontsize=18, labelpad=10)
    ax1.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
    ax1.set_xlabel("Phase w.r.t. Discovery Epoch [Days]", fontsize=18, labelpad=5)
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
    ax1.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=18)
    ax1.invert_yaxis()

    props = dict(boxstyle='round', facecolor='gray', alpha=0.67)
    ax1.text    (0.06, 0.04, f'IAU Name: {iauname}  ---  Spectral Type: {spectyp}  ---  Host z: {redshift}  ---  Host m-M: {distmod}  ---  Features Inferred: {inferred}', transform=plt.gcf().transFigure, fontsize=12.5, verticalalignment='top', bbox=props)

    plt.subplots_adjust(right=0.75)
    plt.subplots_adjust(bottom=0.17)
    
    plt.savefig(f"fastfinder/outputs/{objectId}.png", dpi=fig.dpi, bbox_inches='tight')
    #plt.show()
    plt.close()

    return