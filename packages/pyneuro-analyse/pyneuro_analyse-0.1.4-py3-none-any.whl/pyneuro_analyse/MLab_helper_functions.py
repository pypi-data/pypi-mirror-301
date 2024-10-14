'''
Set of helper functions to use 
'''
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import math
from scipy.ndimage import gaussian_filter, gaussian_filter1d
from matplotlib.axes import Axes
from scipy.optimize import curve_fit
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt
import seaborn as sns



def extract_timestamp_cutouts(trace_to_extr:np.ndarray, 
                              uncor_timestamps:np.ndarray, 
                              baseline:float, 
                              posttime=None,
                              sampling=1,
                              offset=0.0, 
                              z_scored=False, 
                              dff=False,
                              z_scoring_interval:tuple = None)->pd.DataFrame:
    """
        Parameters:
        trace_to_extract: an array containing values of interest (e.g. dF/F trace), ASSUMES CONSTANT SAMPLING FREQUENCY!!

        timestamps: array containing timepoints of the events, points from trace_to_extract will be taken around each timestamp

        baseline: time before the timepoint (in seconds) to be extracted

        posttime: time after the timepoint (in seconds) to be extracted, by default equals baseline

        sampling: acquisition rate of the trace_to-extract, in Hz (by default 1)

        offset: shift in time in seconds between timestamps and trace_to_extract (if, for example photometry acqusition starts 5 seconds before behavior video 
            from which timepoints were annotated offset = 5)

        z-scored: returns cutouts as z-score values computed on baseline

        dff: returns cutouts as deltaF/F values computed on baseline

        Returns:
        DataFrame with signal cutouts around each trigger, organized in columns
    """
    #Copy the input trace
    trace_to_extract = trace_to_extr.copy()
    #if time after the trigger is not specified, make it equal to baseline
    if not posttime:
        posttime=baseline
    #if time interval for z-score baseline is not specified, use the whole duration of the baseline
    if z_scoring_interval is None:
        z_scoring_interval = (-baseline,0)
    #Make "result" dataframe
    result=pd.DataFrame()
    #Apply offset to trigger timestamps
    timestamps = uncor_timestamps+offset
    #Define length of the cutout (in points)
    cutout_length =  round((posttime+baseline)*sampling)
    #Define time points of the cutouts relative to the trigger

    cutouts = []
    #Extract cutouts around each trigger in a loop
    for i,timestamp in enumerate(timestamps):
        indfrom = round((timestamp-baseline)*sampling)
        if indfrom<0 or indfrom+cutout_length>len(trace_to_extract):
            continue
        cutouts.append(pd.Series(trace_to_extract[indfrom:indfrom+cutout_length]))

    result = pd.concat(cutouts, axis=1)
    result.index=np.round(np.arange(-baseline,posttime,1/sampling),round(math.log10(sampling)+2))
    
    #Apply deltaF/F0 transformation to all cutouts (columns of results
    if dff:
        for col in result:
            base_mean = result.loc[:0,col].mean()
            result[col]-=base_mean
            result[col]/=base_mean
    #Apply deltaF/F0 transformation to the cutout (columns of results)
    if z_scored:
        z_score_from = result.index[result.index>z_scoring_interval[0]][0]
        z_score_to = result.index[result.index<z_scoring_interval[1]][-1]
        for col in result:
            std = result.loc[z_score_from:z_score_to,col].std()
            result[col]-=result.loc[z_score_from:z_score_to,col].mean()
            result[col]/=std
            
    return result

def extract_timestamp_cutouts_2p(roi_table:pd.DataFrame, 
                                 uncor_timestamps :np.ndarray, 
                                 baseline:float, 
                                 posttime=None,
                                 sampling=1,
                                 offset=0.0, 
                                 z_scored=False, 
                                 dff=False, 
                                 z_scoring_interval:tuple = None)->pd.DataFrame:
    """
        Parameters:
        roi_table: 2d table containing ROI data, 1 ROI per column, ASSUMES CONSTANT SAMPLING FREQUENCY!!

        timestamps: array containing timepoints of the events, points from trace_to_extract will be taken around each timestamp

        baseline: time before the timepoint (in seconds) to be extracted

        posttime: time after the timepoint (in seconds) to be extracted, by default equals baseline

        sampling: acquisition rate of the trace_to-extract, in Hz (by default 1)

        offset: shift in time in seconds between timestamps and trace_to_extract (if, for example photometry acqusition starts 5 seconds before behavior video 
            from which timepoints were annotated offset = 5)

        z-scored: returns cutouts as z-score values computed on baseline

        dff: returns cutouts as deltaF/F values computed on baseline

        Returns:
        DataFrame with signal cutouts around each trigger, for each ROI, organized in columns
    """
    per_ROI_df_list = []
    for i,roi in enumerate(roi_table):
        temp_results = extract_timestamp_cutouts(roi_table[roi].values, uncor_timestamps, baseline, posttime, sampling, offset, z_scored, dff, z_scoring_interval)
        temp_results.columns = [f"ROI{i:02}_{col:02}" for col in temp_results.columns]
        per_ROI_df_list.append(temp_results.T)
    return pd.concat(per_ROI_df_list, axis=0)
    
def locate_onsets_offsets(annotated_trace:np.ndarray, time_trace:np.ndarray = None, thresh=0.5, on_dur_thresh=0, off_dur_thresh=0, return_dur = False)->pd.DataFrame:
    '''
    # Parameters
    annotated_trace: array with behavioral annotations
    time_trace: array of equal length with annotated_trace, providing timing information on every point. If not provided, assumes 1 second for each point in annotated_trace
    thresh: Threshold to separate ON and OFF states of the trace, Default = 0.5 (separates above and below)
    on_dur_threh: removes all ON bouts with shorter duration than this parameter (in s), merges OFF bouts
    off_dur_thresh: removes all OFF bouts shorter that this parameter (in s), merges ON bouts
    return_dur: append column with durations of ON bouts

    #Returns
    Table with onsets (column 1), offsets (column 2) timings, and if return_dur=True durations of active state (column 3)
    '''
    if time_trace is None:
        time_trace = np.arange(len(annotated_trace))
    onsets = time_trace[(annotated_trace>thresh) & (np.roll(annotated_trace,1)<=thresh)]
    offsets = time_trace[(annotated_trace<thresh) & (np.roll(annotated_trace,1)>=thresh)]

    
    if onsets[-1] == time_trace[-1]:
        onsets = onsets[:-1]
    if offsets[-1]==time_trace[-1]:
        offsets = offsets[:-1]


    if offsets[0]<onsets[0]:
        offsets = np.roll(offsets,-1)

    
    if len(onsets)< len(offsets):
            onsets=np.append(onsets,float("nan"))
    elif len(onsets)> len(offsets):
        offsets=np.append(offsets,float("nan"))

    if off_dur_thresh>0:
        off_durations=onsets-np.roll(offsets,1)
        indices_to_remove=np.arange(len(onsets))
        indices_to_remove = indices_to_remove[off_durations<off_dur_thresh][1:]
        onsets=np.delete(onsets,indices_to_remove)
        offsets=np.delete(offsets,indices_to_remove-1)

    if on_dur_thresh>0:
        on_durations=offsets-onsets
        indices_to_remove=np.arange(len(onsets))
        indices_to_remove = indices_to_remove[on_durations<on_dur_thresh]
        onsets=np.delete(onsets,indices_to_remove)
        offsets=np.delete(offsets,indices_to_remove)

    results = pd.concat([pd.Series(onsets), pd.Series(offsets)],axis=1)
    results.columns = ["on","off"]
    if return_dur:
        results["duration"] = results.off-results.on
    return results


def create_timestamp_aligned_video(video:np.ndarray, 
                                   timestamps:np.ndarray, 
                                   FPS:int, 
                                   baseline:float, 
                                   posttime:float, 
                                   bin_factor=1, 
                                   gaussian_smoothing=None, 
                                   z_scored=False,
                                   z_scoring_interval:tuple = None):
    """
    # Parameters
    video: 3d array (time being the first dimension) from which to make an aligned movie
    timestamps: a list of timestamps (in seconds) to which to align the video
    FPS: sampling frequency in Hz
    baseline: duration of cutout before alignment point, in seconds
    posttime: duration of cutout afte the alignment point, in seconds
    bin_factor: optional, perform spatial n x n binning on the resulting video. Default: 1 - no binning 
    gaussian_smoothing: optional, kernel for the gaussian filter (smoothes both in space !!AND TIME!!). Default: None - no smoothing
    z_scored: if True, z-scores the movie, mean and std for z-scoring are calculated on the "z-scoring interval". Default: False
    z-scoring_interval: if not None, a pair of values denoting the interval in which to calculate the mean and std for z-scoring, in seconds, relative to the alignment point 0,
    e.g. (-3,0) will use all points 3 seconds before the alignemtn point (including -3). if None, uses the whole duration of the baseline. Default: None

    # Returns
    A video (3d array) aligned to the 
    """
    excerpts = []
    omitted_count = 0
    if z_scoring_interval is None:
        z_scoring_interval = (-baseline,0)

    for timestamp in timestamps:
        if timestamp>=baseline and timestamp<=len(video)/FPS-posttime:
            from_frame = int((timestamp-baseline)*FPS)
            to_frame = int((timestamp+posttime)*FPS)
            excerpts.append(video[from_frame:to_frame,:,:])

    if omitted_count:
        print("{} timestamps omitted due to being too close to the start/end of the video, shorten baseline/posttime parameters to reinclude them.".format(omitted_count))

    if len(excerpts):
        aligned_video = np.array(excerpts).mean(axis=0)
        if bin_factor>1:
            aligned_video = space_bin(aligned_video,bin_factor)
        if gaussian_smoothing is not None:
            aligned_video = gaussian_filter(aligned_video, gaussian_smoothing)
        if z_scored:
            aligned_video = (aligned_video-aligned_video[int((baseline+z_scoring_interval[0])*FPS):int(baseline*FPS)].mean(axis=0))\
                /aligned_video[:int((baseline+z_scoring_interval[1])*FPS)].std(axis=0)
        return aligned_video


def z_score_trace(trace: np.ndarray, z_scoring_interval:tuple=None, gaussian_smoothing = None):
    scaler = StandardScaler()
    if z_scoring_interval is None:
        z_scoring_interval = (0, len(trace))
    #scaler.fit(trace[z_scoring_interval[0]:z_scoring_interval[1]])
    std = trace[z_scoring_interval[0]:z_scoring_interval[1]]
    z_trace = (trace - trace[z_scoring_interval[0]:z_scoring_interval[1]].mean())/std
    if gaussian_smoothing is not None:
        z_trace = gaussian_filter1d(z_trace, gaussian_smoothing)
    return z_trace
    #return scaler.transform(scaler)
 

def bin_trace(trace:np.ndarray, binwidth=1, just_smooth=False):
    if binwidth>1:
        numpnts = (len(trace)//binwidth) *binwidth
        trace = np.insert(trace, 0 , [trace[0] for _ in range(binwidth)])
        trace = np.append(trace, [trace[-1] for _ in range(binwidth)])
        new_trace = trace.copy()
        
        for i in range(1,binwidth):
            new_trace+=np.roll(trace,-i)
        if just_smooth:
            return np.roll(new_trace/binwidth,binwidth//2)[binwidth:-binwidth]
        else:
            return new_trace[binwidth:-binwidth][0:numpnts:binwidth]/binwidth
    else:
        return trace
    
def space_bin(video, bin=2):

    binrate = bin
    binned_video = video.copy()
    for i in range(1,bin):
        binned_video+=np.roll(binned_video,-i,axis=1)
        binned_video+= np.roll(binned_video,-i,axis=2)  
    return binned_video[:,::binrate,::binrate]/(bin**2)

def extract_response_parameters(trace:pd.Series, 
                                response_type="mean",
                                no_resp_thresh:float=0, 
                                subtract_baseline=False,
                                baseline_time_interval:tuple=None,
                                response_time_interval:tuple=None,
                                gaussian_smoothing:float=0,
                                plateau_thresh:float=0.9,
                                save_figure:str=None,
                                show_figure=False):
    '''
    # Parameters
    response_type: mean or peak
    '''
    def extract_response_parameters_1d(trace:pd.Series,
                                       response_type="mean",
                                       no_resp_thresh:float=0,
                                       subtract_baseline=False,
                                       baseline_time_interval:tuple=None,
                                       response_time_interval:tuple=None,
                                       gaussian_smoothing:float=0,
                                       plateau_thresh:float=0.9,
                                       ax:Axes=None):

        resp={}
        baseline = trace[trace.index[np.where((trace.index>=baseline_time_interval[0]) & (trace.index<=baseline_time_interval[1]))]].mean()
        if subtract_baseline:
            trace-=baseline
        #extract AUC
        if response_type=="mean":
            resp["mean"] = trace[trace.index[np.where((trace.index>=response_time_interval[0]) & (trace.index<=response_time_interval[1]))]].mean()
            #resp["AUC"]*= abs(response_time_interval[1]-response_time_interval[0])
        #extract peak

        elif response_type=="peak":
            resp["peak"] = trace[trace.index[np.where((trace.index>=response_time_interval[0]) & (trace.index<=response_time_interval[1]))]].max()

        resp[f"{response_type}_above_thresh"] = np.nan if resp[f"{response_type}"]< no_resp_thresh else resp[f"{response_type}"]

        if ax is not None:
            ax.plot(trace)
            ax.plot([baseline_time_interval[0],baseline_time_interval[1]],[0,0],color='k', linewidth=2)
            ax.plot([response_time_interval[0],response_time_interval[1]],[resp[response_type],resp[response_type]],color='r', linewidth=2)
            ax.axvline(x=0, color='k', linestyle='dashed', linewidth=0.5)

        if resp[f"{response_type}_above_thresh"] is np.nan:
            resp["latency"]=np.nan
            resp["tau_decay"]=np.nan
            resp["plateau_dur"]=np.nan
        else:
            #smooth trace
            if gaussian_smoothing:
                trace.loc[:] = gaussian_filter1d(trace, gaussian_smoothing)
            
            if ax is not None:
                ax.plot(trace, linestyle='dashed')
            #extract latency
            #peak_loc = trace[trace.index[np.where((trace.index>=response_time_interval[0]) & (trace.index<=response_time_interval[1]))]].idxmax()
            peak_loc = trace[(trace.index>=response_time_interval[0]) & (trace.index<=response_time_interval[1])].idxmax()
            peak = trace[(trace.index>=response_time_interval[0]) & (trace.index<=response_time_interval[1])].max()
            trace/=peak
            resp["latency"] = trace.index[np.where((trace.values<0.5) & (trace.index<=peak_loc))][-1]

            #extract plateau duration
            try:
                plateau_from = trace.index[np.where((trace.values<plateau_thresh) & (trace.index<=peak_loc))][-1]
                plateau_to = trace.index[np.where((trace.values<plateau_thresh) & (trace.index>=peak_loc))][0]
                resp["plateau_dur"] = plateau_to - plateau_from
            except:
                resp["plateau_dur"] = np.nan

            #extract tau decay

            # Curve fitting function
            def fit_func(x, a,b,c):
                #nonlocal peak
                return np.clip(b*np.exp(-(x-c)/a),0,1)
            
            fit_to = trace.index[np.where((trace.values>=0.5) & (trace.index>=peak_loc))][-1]
            if len(trace[(trace.index>=peak_loc) & (trace.index<=fit_to)])>10:
                fit_trace = trace[peak_loc:fit_to]
            else:
                fit_trace = trace[peak_loc:].iloc[:10]
            
            try:
                params = curve_fit(fit_func, fit_trace.index.values, fit_trace.values, [1,1,0]);
                if params[1][0,0]<3:
                    resp["tau_decay"]=params[0][0]
                    if ax is not None:
                        ax.plot(fit_trace.index,[fit_func(i,params[0][0],params[0][1],params[0][2])*peak for i in fit_trace.index], linewidth=2, color='k', linestyle='dashed')
                else:
                    resp["tau_decay"]=np.nan
                
            except:
                resp["tau_decay"]=np.nan

        return pd.DataFrame(resp, index=[0])


    if response_time_interval is None:
        response_time_interval = (0,trace.index[-1])
    else:
        response_time_interval = np.clip(response_time_interval,trace.index[0],trace.index[-1])
    
    if baseline_time_interval is None:
        baseline_time_interval = (trace.index[0],0)
    else:
        baseline_time_interval = np.clip(baseline_time_interval,trace.index[0],trace.index[-1])

    if len(trace.shape)==1:
        fig = plt.figure(figsize=(3,3))
        ax = fig.add_subplot(111)
        res = extract_response_parameters_1d(trace.copy(), response_type, no_resp_thresh, subtract_baseline, baseline_time_interval, response_time_interval, gaussian_smoothing, plateau_thresh ,ax=ax)
        sns.despine()
        fig.show
        if save_figure is not None:
            fig.savefig(save_figure)
        return res
    else:
        res_list = []
        nrows = math.ceil(np.sqrt(trace.shape[1]))
        ncols = math.ceil(trace.shape[1]/nrows)
        fig,axes = plt.subplots(nrows,ncols,figsize=(2*nrows,2*ncols))
        ax_counter = 0
        for roi in trace:
            res = extract_response_parameters_1d(trace[roi].copy(), 
                                                 response_type, 
                                                 no_resp_thresh, 
                                                 subtract_baseline, 
                                                 baseline_time_interval, 
                                                 response_time_interval, 
                                                 gaussian_smoothing, 
                                                 plateau_thresh,
                                                 ax=axes[ax_counter//ncols, ax_counter%ncols])
            res_list.append(res)
            ax_counter+=1

        result = pd.concat(res_list)
        result.index=trace.columns

        ax_counter = 0
        for roi in trace:
            axes[ax_counter//ncols, ax_counter%ncols].yaxis.set_major_locator(plt.MaxNLocator(4))
            axes[ax_counter//ncols, ax_counter%ncols].set_title(f"{roi}: {result.loc[roi,response_type]:.2f} resp.", fontsize=6)
            axes[ax_counter//ncols, ax_counter%ncols].set_ylim((-2*result[f"{response_type}_above_thresh"].median(skipna=True),4*result[f"{response_type}_above_thresh"].median(skipna=True)))
            axes[ax_counter//ncols, ax_counter%ncols].tick_params(axis="y", labelsize=5)
            axes[ax_counter//ncols, ax_counter%ncols].spines['bottom'].set_position('zero')
            ax_counter+=1

        sns.despine()
        #fig.show
        if save_figure is not None:
            fig.savefig(save_figure)
        if not show_figure:
            plt.close(fig)
        return result

def calculate_response_statistics(response_data_table:pd.DataFrame,
                                  response_type:str="mean",
                                  groups:pd.Series=None,
                                  save_figure:str=None,
                                  show_figure=False)->pd.DataFrame:
    
    response_data_table = response_data_table.copy()
    cols = response_data_table.columns
    stats = {}
    if groups is not None:
        response_data_table["gr"] = groups.values
        response_data_table = response_data_table.groupby("gr")

    stats[response_type+"_average"] = response_data_table[response_type].mean()
    stats[response_type+"_std"] = response_data_table[response_type].std()
    stats[response_type+"_sem"] = response_data_table[response_type].sem()

    stats[response_type+"_above_thresh_average"] = response_data_table[response_type+"_above_thresh"].mean()
    stats[response_type+"_above_thresh_std"] = response_data_table[response_type+"_above_thresh"].std()
    stats[response_type+"_above_thresh_sem"] = response_data_table[response_type+"_above_thresh"].sem()

    if "latency" in cols:
        stats["latency_average"] = response_data_table["latency"].mean()
        stats["latency_std"] = response_data_table["latency"].std()
    if "tau_decay" in cols:
        stats["tau_decay_average"] = response_data_table["tau_decay"].mean()
        stats["tau_decay_std"] = response_data_table["tau_decay"].std()
    if "plateau_dur" in cols:
        stats["plateau_dur_average"] = response_data_table["plateau_dur"].mean()
        stats["plateau_dur_std"] = response_data_table["plateau_dur"].std()

    stats["reliability"] = response_data_table[response_type+"_above_thresh"].count() / response_data_table[response_type].count()

    if groups is None:
        stats["wilc_p_value"] = wilcoxon(response_data_table[response_type].values, np.zeros_like(response_data_table[response_type].values)).pvalue

        fig,axes=plt.subplots(1,5, figsize=(5,2))
        for i,metric in enumerate(response_data_table):
            sns.boxplot(response_data_table[metric].dropna(),ax=axes[i])
            sns.swarmplot(y=response_data_table[metric].dropna(),ax=axes[i],s=2)
        sns.despine()
        plt.tight_layout()
        if not show_figure:
            plt.close(fig)

        return pd.DataFrame(stats, index=["population"])
    else:
        stats["wilc_p_value"] = response_data_table[response_type].apply(lambda x: wilcoxon(x,np.zeros_like(x)).pvalue)

        fig,axes=plt.subplots(5,1, figsize=(len(groups.unique())//2,10))
        for i,metric in enumerate(response_data_table.obj.drop(columns="gr")):
            sns.boxplot(response_data_table.obj,y=metric, x="gr", hue='gr',ax=axes[i])
            sns.swarmplot(response_data_table.obj,y=metric,ax=axes[i],x="gr",color='k',s=2, edgecolor='w', linewidth=0.2);
        sns.despine()
        plt.tight_layout()
        if not show_figure:
            plt.close(fig)
        return pd.DataFrame(stats)