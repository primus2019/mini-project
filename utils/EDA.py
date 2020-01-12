import numpy as np
import pandas as pd

from statsmodels.stats.outliers_influence import variance_inflation_factor


def feature_VIF(ds, features='all', encoding='utf-8', header=0, index_col=0):
    ds = pd.read_csv(ds, encoding=encoding, header=header, index_col=index_col) if isinstance(ds, str) else ds
    if features == 'all':
        features = ds.columns.values.tolist()
    else:
        features = [features] if isinstance(features, str) else features
    
    inputs = np.hstack((ds.loc[:, features], np.ones((ds.shape[0], 1))))
    # printlog('inputs: {}'.format(inputs[:5, -10:]))
    # printlog([variance_inflation_factor(ds.loc[:, features].values, i) for i in range(10)])
    vif = pd.DataFrame([variance_inflation_factor(inputs, i) for i in range(len(features))], index=features, columns=['vif'])
    # printlog(vif.head(50))
    return vif