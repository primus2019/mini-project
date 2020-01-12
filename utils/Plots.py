import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from .EDA import feature_VIF


def correlationPlot(ds, features, savefig, title=None):
    features = ds.columns.values.tolist() if features == 'all' else features
    corr = ds.loc[:, features].corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(24, 20))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    if title:
        plt.title(title)
    plt.savefig(savefig)


def vifPlot(ds, features, savefig, title=None):
    features = ds.columns.values.tolist() if features == 'all' else features
    vif = pd.DataFrame(np.zeros((ds.shape[1], ds.shape[1])), index=ds.columns.values, columns=ds.columns.values)
    for f1 in features:
        for f2 in features:
            if f1 != f2:
                # print(f1, ' ', f2)
                temp_vif = feature_VIF(ds, features=[f1, f2]).values.tolist()[0][0]
                vif.loc[f1, f2] = temp_vif
    # print(vif)
    mask = np.zeros_like(vif, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(24, 20))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(vif, mask=mask, cmap=cmap, robust=True, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    if title:
        plt.title(title)
    plt.savefig(savefig)


def jointPlot(ds, f1, f2, savefig, title='default', logarithmic=False):
    sns.set(style="ticks")
    if logarithmic:
        p = sns.jointplot(ds[[f1]], ds[[f2]], kind="reg", color="#4CB391", logx=logarithmic)
        # p.ax_joint.set_xscale('log')
        # p.ax_joint.set_yscale('log')
    else:
        p = sns.jointplot(ds[[f1]], ds[[f2]], kind="hex", color="#4CB391")
    # if title == 'default':
    #     title = 'Marginal distributions between {} and {}'.format(f1, f2)
    # plt.title(title)
    plt.savefig(savefig)
