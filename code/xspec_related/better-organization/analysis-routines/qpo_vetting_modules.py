#spell-checker: disable

## QPO Finder 

def hunter(
    full_id:str,
    image_df_dir:str='./code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw', 
    data_dir:str='./code/xspec_related/qpo_routines/jan-1-2022/final_logs/'): 
    
    import numpy as np
    import pandas as pd
    from scipy.signal import find_peaks
    
    image_df = image_df_dir + '/' + full_id + '.csv'
    (x,y) = (np.array(image_df[i]) for i in ['x', 'y'])

    df = pd.read_csv(data_dir+'/'+full_id+'.csv')

    freqs = np.array(df['freq'])
    norms = np.array(df['norm'])
    widths = np.array(df['fwhm'])
    fit_stats = np.array(df['fit_stat'])

    # Rec chi. "peaks" aka valleys
    neg_fit_stats = -1*fit_stats
    min_height = np.min(neg_fit_stats)+14
    initial_peak_indices, _ = find_peaks(neg_fit_stats, height=min_height)
    canidate_peaks_mask = np.logical_or(freqs[initial_peak_indices]>1.2, freqs[initial_peak_indices]<0.8) # originally 0.9-1.1 ? 

    canidate_peak_indices = initial_peak_indices[canidate_peaks_mask]
    canidate_freqs = freqs[canidate_peak_indices]
    canidate_chis = fit_stats[canidate_peak_indices]
    canidate_widths = widths[canidate_peak_indices]
    canidate_norms = norms[canidate_peak_indices]

    canidate_rms_powers = [y[np.argmin(np.abs(x - freq))] for freq in canidate_freqs] # fundamental is chosen as maximum rms power peak 

    fundamental_index = np.argmax(canidate_rms_powers)
    fundamental_freq = canidate_freqs[fundamental_index]

    harmonic_statuses = []

    # Evaluate harmonic statuses 
    for canidate_index, canidate in enumerate(canidate_freqs): # within 2% !! 
        if canidate_index!=fundamental_index: 
            not_harmonic = True 
            for n in range(2,5): 
                harmonic = n*fundamental_freq
                subharmonic = fundamental_freq/n

                if canidate/harmonic < 1.02 and canidate/harmonic > 0.98: 
                    harmonic_statuses.append('h') # for harmonic (isn't this technicall the "second harmonic")
                    not_harmonic = False
                    break

                elif canidate/subharmonic < 1.02 and canidate/subharmonic > 0.98:
                    harmonic_statuses.append('s') # for sub-harmonic
                    not_harmonic = False
                    break

            if not_harmonic: 
                harmonic_statuses.append('n') # for "N"-ot harmonic
        
        else: 
            harmonic_statuses.append('f') # for fundamental, of course 

    str_freqs = ['Freq: '+str(round(i,3)) for i in canidate_freqs]

    for counter, str_freq in enumerate(str_freqs): 
        harmonic_status = harmonic_statuses[counter]
        if harmonic_status == 's': 
            str_freqs[counter] = str_freq+'; subharmonic'

        elif harmonic_status == 'h': 
            str_freqs[counter] = str_freq+'; harmonic'

        elif harmonic_status == 'f': 
            str_freqs[counter] = str_freq+'; fundamental'

        else: 
            str_freqs[counter] = str_freq+'; not harmonic or fundamental'


    canidate_dict = {'canidate_indices':canidate_peak_indices, # indices correspond to the ~268 logarithmically spaced frequencies array used in xspec  
                        'canidate_freqs':canidate_freqs, 
                        'canidate_chis':canidate_chis,
                        'canidate_widths':canidate_widths, 
                        'canidate_norms':canidate_norms, 
                        'canidate_rms_powers':canidate_rms_powers, 
                        'fundamental_index':fundamental_index}

    labels_dict = {'harmonic_status':harmonic_statuses, 
                    'canidate_labels':str_freqs}

    return canidate_dict, labels_dict

## Plotting functions

def make_vetting_plot(
    full_id:str, 
    image_df_dir: str='./code/xspec_related/post-processing/initial/pds_plots/plot_dir/plot_data_raw', # I usually zip this dirs when saving to GitHub
    qpo_df_dir: str='./code/xspec_related/qpo_routines/jan-1-2022/final_logs', 
    canidates_dict: float={}, 
    annotations_dict: str={},
    plot_dir: str='none',  
    ignore_range: float=[0.8,1.2]):

    """
    Args: 
        annotations_dict: two item dictionary; first array should be initial algorithmic annotations; second array should be human annotations
        ignore_range: inclusive range of frequencies in which peak detection should be excluded from. Default is [0.8-1.2]
    
    Returns: 
    """

    '''IMPORTS'''
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    # get arrays

    image_df = image_df_dir + '/' + full_id + '.csv'
    (x,y,xerr,yerr) = (np.array(image_df[i])for i in ['x', 'y', 'xerr', 'yerr'])

    fitted_labels = ['freq', 'norm', 'fwhm', 'fit_stat']
    qpo_df = qpo_df_dir +'/'+full_id+'.csv'
    (freqs, norms, widths, fit_stats) = (np.array(qpo_df[i]) for i in fitted_labels)

    min_freq, max_freq = np.min(freqs), np.max(freqs)

    canidate_labels = ['canidate_indices', 'canidate_chis', 'canidate_widths', 'canidate_norms']
    (peak_freqs, peak_chis, peak_widths, peak_norms) = (np.array(canidates_dict[i]) for i in canidate_labels)
    fundamental_index = canidates_dict['fundamental_index']

    if len(annotations_dict)>0: 

        fig = plt.figure(constrained_layout=True, figsize=(7,4), sharex=True)
        mosaic = """
            AB
            CD
            EF
            """

    else: 
        fig = plt.figure(constrained_layout=True, figsize=(7,2.6), sharex=True)
        mosaic = """
            AB
            CD
            """

    ax_dict = fig.subplot_mosaic(mosaic)

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for ax_str in ax_dict: 
        ax = ax_dict[ax_str]
        ax.set(xlim=(0.1,20), xscale='log', yscale='log', xlabel='Frequency [Hz]')
        ax.axvspan(ignore_range[0],ignore_range[1], color='red', alpha=0.15, zorder=1)

        if ax_str == 'C' or ax_str == 'D':
            ax.errorbar(x,y,xerr=xerr, yerr=yerr, c=colors[0], lw=0.5, ms=2, marker='o')
            ax.set_ylim(bottom=10**-5)


    # Fit Stats
    
    ax = ax_dict['A']
    
    ax.scatter(freqs, fit_stats, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
    ax.hlines(y=np.max(fit_stats)-14, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}10$', color='black', ls='--')
    ax.hlines(y=np.max(fit_stats)-24, xmin=min_freq, xmax=max_freq, label='Max'+r'$-\Delta\mathrm{AIC}20$', color='black', ls='--')
    ax.scatter(peak_freqs, peak_chis, color='C1', marker='x', s=20)
    
    ax.set_ylabel('Fit Statistic')

    ax = ax_dict['B']

    ax.scatter(freqs, norms, color='#408ee0', s=6, linewidths=0.3, edgecolors='black')
    ax.set_ylabel('Norm.')
    
    min_norm, sigma_norm = np.min(norms), np.std(norms)
    
    ax.hlines(y=min_norm+sigma_norm,  xmin=min_freq,  xmax=max_freq, label='Min '+r'$+1\sigma$')
    ax.hlines(y=min_norm+2*sigma_norm,  xmin=min_freq,  xmax=max_freq, label='Min '+r'$+2\sigma$')
    
    for ax in [ax_dict['A'], ax_dict['B']]:
        ax.legend(loc='upper left', fontsize='x-small')

    # D --> best fit models 
    # loren(E, EL, σ, K):
    
    ax = ax_dict['D']

    ax.plot(image_df.e, image_df.total)

    def loren(E, EL, σ, K):
        return K*(σ/(2*3.1415659265))/((E-EL)**2+(σ/2)**2)

    for canidate_index in range(len(peak_widths)): 
        canidate_freq = peak_freqs[canidate_index]
        canidate_width = peak_widths[canidate_index]
        canidate_norm = peak_norms[canidate_index]
        x_range = np.linspace(0.85*canidate_freq, 1.15*canidate_freq, 50)

        y_loren = loren(x_range, canidate_freq, canidate_width, canidate_norm)

        ax.plot(x_range, y_loren, color='orange', lw=1)

    fundamental_freq = peak_freqs[fundamental_index]
    for n in range(2,5): 
        harmonic = n*fundamental_freq
        subharmonic = fundamental_freq/n

        ax.axvline(x=harmonic, ymin=0.9, ymax=1, color='green')
        ax.axvline(x=subharmonic, ymin=0.9, ymax=1, color='green')
        
    # Annotations Info
    if len(annotations_dict)>0: 

        annotations_key = list(annotations_dict.keys())

        ax = ax_dict['E']
        ax.axis('off')
        ax.set(title='Detected QPO Frequencies')

        freqs_str = '\n'.join(annotations_dict[annotations_key[0]])

        ax.text(0., 0.25, freqs_str)

    if len(annotations_dict>1): 

        thoughts_str = '\n'.join(annotations_dict[annotations_key[1]])
        ax.text(0., 0.25, thoughts_str)

        ax = ax_dict['F']
        ax.axis('off')
  
    if plot_dir != 'none': 
        plot_path = plot_dir + '/'+full_id+'.png'
        plt.savefig(plot_path,bbox_inches='tight', dpi=150)

    else: 
        plt.show()

    plt.clf()
    plt.close()