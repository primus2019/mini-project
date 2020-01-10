import geocoder
import folium
import folium.plugins
import pandas as pd



# # create location counter
# features = ['WORK_CITY', 'WORK_PROVINCE', 'WORK_COUNTRY']
# ds = pd.read_csv('data/database2.csv', header=0, index_col=0)
# ds = ds.loc[:, features]
# ds = ds.fillna(' ')
# location = ds['WORK_CITY'] + ', ' + ds['WORK_PROVINCE'] + ', ' + ds['WORK_COUNTRY']
# location_counter = location.value_counts()
# location_counter.to_csv('data/location_counter.csv', header='location counts')
# print(location_counter.head())

# # add latitude-longtitude data to counter
# ds = pd.read_csv('data/location_counter.csv', header=0, index_col=0)
# latlng = []
# for location in ds.index.values.tolist():
#     print(location)
#     latlng.append(geocoder.arcgis(location).latlng)
# latlng = pd.DataFrame({'latlng': latlng}, index=ds.index.values)
# ds = pd.concat([ds, latlng], axis=1, sort=True)
# ds.to_csv('data/loc_cnt_latlng.csv')

# # plot heatmap
# from ast import literal_eval
# basemap = folium.Map(location=[31.2304, 121.4737], zoom_start=3)
# ds = pd.read_csv('data/loc_cnt_latlng.csv', header=0, index_col=0).dropna()
# temp = pd.DataFrame(ds.loc[:, 'latlng'].apply(literal_eval).values.tolist(), index=ds.index.values, columns=['lat', 'lng'])
# ds = pd.concat([temp, ds['0']], axis=1, sort=True)
# print(ds[['lat', 'lng', '0']].groupby(['lat', 'lng']).sum().reset_index().head())
# folium.plugins.HeatMap(data=ds[['lat', 'lng', '0']].groupby(['lat', 'lng']).sum().reset_index().values.tolist()).add_to(basemap)
# basemap.save('plots/heatmap.html')