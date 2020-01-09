import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
import datetime

from collections import Counter

def run():
    ds = pd.read_csv('data/database2.csv', header=0, index_col=0)
    print('**1.  features with na data and na data numbers\n{}'.format(ds.isna().sum()[ds.isna().sum() != 0]))
    print('**2.  feature data type\n{}'.format(dict(Counter(ds.dtypes.values.tolist()))))
    print('**3.  deal with non-numeric feature')
    print('**3.1 a glance at non-numeric data')
    non_numeric_features = ds.loc[:, ds.dtypes == np.dtype('O')].columns.values
    print(ds.loc[:, non_numeric_features].head())
    print('**3.2 fill datetime feature data with datetime')
    datetime_features = ['FFP_DATE', 'FIRST_FLIGHT_DATE', 'LOAD_TIME', 'LAST_FLIGHT_DATE', 'TRANSACTION_DATE']
    for feature in datetime_features:
        ds.loc[:, feature] = pd.to_datetime(ds.loc[:, feature], infer_datetime_format=True)
    print('**3.3 remaining non-numeric features')
    non_numeric_features = ds.loc[:, ds.dtypes == np.dtype('O')].columns.values
    print(ds.loc[:, non_numeric_features].head())
    print('**3.4 replace "GENDER" with 0-1 numeric data')
    ds.loc[:, 'GENDER'] = ds.loc[:, 'GENDER'].apply(lambda item: 1 if item == '男' else 0)
    print('**3.5 remaining non-numeric features')
    non_numeric_features = ds.loc[:, ds.dtypes == np.dtype('O')].columns.values
    print(ds.loc[:, non_numeric_features].head())
    print('**3.6 record and non-numeric data')
    geometric_features = ['WORK_CITY', 'WORK_PROVINCE', 'WORK_COUNTRY']
    for feature in geometric_features:
        with open(f'records/{feature}.txt', 'w+', encoding='utf-8') as file:
            for value, count in dict(Counter(ds.loc[:, feature].values.tolist())).items():
                file.write(f'{value}: \t{count}\n')
    ds = ds.drop(columns=geometric_features)
    print('**3.7 feature data type\n{}'.format(dict(Counter(ds.dtypes.values.tolist()))))
    print('**4.  deal with numeric features')
    print('**4.1 fill na data in numeric feature with -1')
    numeric_na_features = ['age', 'EXPENSE_SUM_YR_1', 'EXPENSE_SUM_YR_2']
    ds.loc[:, numeric_na_features] = ds.loc[:, numeric_na_features].fillna(-1)
    numeric_features = ds.loc[:, (ds.dtypes == np.dtype('int64')) & (ds.dtypes == np.dtype('float64'))].columns.values
    print('**4.2 check outlier data in numeric feautures')
    for feature in numeric_features:
        temp = ds.loc[:, feature]
        print(f'{feature}: \t{temp[np.abs(temp - temp.mean()) >= 3 * temp.std()]}')
    print('**4.3 nothing printed; there is obviously no outlier data in numeric features')
    print('**5.  store cleaned dataset into data/dataset.csv')
    ds.to_csv('data/data.csv')




if __name__ == '__main__':
    run()