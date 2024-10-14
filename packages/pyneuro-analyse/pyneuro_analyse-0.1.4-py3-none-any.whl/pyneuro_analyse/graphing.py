import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_heatmap(axes:plt.Axes, 
                 data:pd.DataFrame, 
                 colfrom=None, 
                 colto=None, 
                 title="Heatmap",
                 cbar_title = "deltaF/F", 
                 vmin=-0.3, 
                 vmax=0.3, 
                 skipticks=5,
                 cmap="coolwarm",
                 trigger_onset=15,
                 cbar=True,
                 **kwargs):
    ax=sns.heatmap(data.loc[:,colfrom:colto], ax=axes, vmin=vmin, vmax=vmax, cmap=cmap, cbar=False, cbar_kws={'label':cbar_title, 'aspect':40, 'pad':0.01},**kwargs)
    if cbar:
        colorbar(ax.get_children()[0], cbar_title)
        
    ax.set_title(title)
    ax.axvline(x=trigger_onset, linestyle='dashed', linewidth=1, color='k')
        
    ax.set_xticks(ax.get_xticks()[::skipticks])
    ax.set_yticks(ax.get_yticks()[::skipticks])
    ax.set_yticklabels(["{}".format(round(i)) for i in ax.get_yticks()],fontsize=8)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("" )
    return ax



def plot_av_trace(
        axes:plt.Axes, 
        data:pd.DataFrame, 
        x:str,
        y:str, 
        title="Average dF/F", 
        xlim=None, 
        ylim=None, 
        ytitle="dF/F", 
        xtitle="Time (s)", 
        plot_individual=False,
        color='k',
        **kwargs):
    if plot_individual:
        ax = sns.lineplot(data=data,x=x,y=y, units=plot_individual, estimator=None, alpha=0.1, color=color)
    ax = sns.lineplot(data=data,x=x,y=y, ax=axes,errorbar=('se',1), color=color, **kwargs)
    if xlim:
        ax.set_xlim(xlim[0],xlim[1])
    if ylim:
        ax.set_ylim(ylim[0],ylim[1])
    else:
        ax.set_ylim(0)

    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)

#    ax.set_xticks([i for i in range(-3,9,3)])
#    ax.axvline(x=0, linestyle='dashed', linewidth=2, color='k')
    ax.spines['bottom'].set_position('zero')
#    ax2.fill_between(x=all_roi_av["Time"], y1 = all_roi_av["dF/F"] - all_roi_av["sem"], y2 = all_roi_av["dF/F"] + all_roi_av["sem"], alpha=0.2, color='k')
    ax.set_title(title)
    return ax


def colorbar(mappable, cbar_label=""):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    import matplotlib.pyplot as plt
    last_axes = plt.gca()
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.02)
    cbar = fig.colorbar(mappable, cax=cax, label=cbar_label)
    cbar.set_label(cbar_label, labelpad=-0.5)
    plt.sca(last_axes)
    return cbar