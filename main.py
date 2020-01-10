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

    print('**6.  plot location distribution')
    print('**6.1 count locations')
    features = ['WORK_CITY', 'WORK_PROVINCE', 'WORK_COUNTRY']
    ds = pd.read_csv('data/database2.csv', header=0, index_col=0)
    ds = ds.loc[:, features]
    ds = ds.fillna(' ')
    location = ds['WORK_CITY'] + ', ' + ds['WORK_PROVINCE'] + ', ' + ds['WORK_COUNTRY']
    location_counter = location.value_counts()
    location_counter.to_csv('data/location_counter.csv', header='location counts')
    print(location_counter.head())

    # WARNING: THIS STEP MAY TAKE HOURS FOR GEOMETRIC REQUIRES AND REQUIRES STABLE INTERNET CONNECTION
    print('**6.2 add latitude-longtitude data to countings')
    ds = pd.read_csv('data/location_counter.csv', header=0, index_col=0)
    latlng = []
    for location in ds.index.values.tolist():
        print(location)
        latlng.append(geocoder.arcgis(location).latlng)
    latlng = pd.DataFrame({'latlng': latlng}, index=ds.index.values)
    ds = pd.concat([ds, latlng], axis=1, sort=True)
    ds.to_csv('data/loc_cnt_latlng.csv')

    print('**6.3 plot heatmap on latitude-longtitude data and countings')
    from ast import literal_eval
    basemap = folium.Map(location=[31.2304, 121.4737], zoom_start=3)
    ds = pd.read_csv('data/loc_cnt_latlng.csv', header=0, index_col=0).dropna()
    temp = pd.DataFrame(ds.loc[:, 'latlng'].apply(literal_eval).values.tolist(), index=ds.index.values, columns=['lat', 'lng'])
    ds = pd.concat([temp, ds['0']], axis=1, sort=True)
    print(ds[['lat', 'lng', '0']].groupby(['lat', 'lng']).sum().reset_index().head())
    folium.plugins.HeatMap(data=ds[['lat', 'lng', '0']].groupby(['lat', 'lng']).sum().reset_index().values.tolist()).add_to(basemap)
    basemap.save('plots/heatmap.html')


if __name__ == '__main__':
    run()