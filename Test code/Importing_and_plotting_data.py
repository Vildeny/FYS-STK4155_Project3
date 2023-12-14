# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 09:32:04 2023

@author: vildesn
"""

import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns

data_path = r'C:\Users\vildesn\OneDrive - Institutt for Energiteknikk\Documents\Ciel_et_Terre\Marlenique\data_analysis\Weather_Station_Data.dat'

data = pd.read_csv(data_path, delimiter=',', 
                   header=1, skiprows=[2, 3], na_values="NAN")

data.index = pd.to_datetime(data["TIMESTAMP"], format="%Y-%m-%d %H:%M:%S")

#%%

plt.figure()
plt.plot(data.index, data["GHI_Avg"], label="GHI")
plt.plot(data.index, data["GTI_Avg"], label="GTI")
plt.plot(data.index, data["RHI_Avg"], label="RHI")

plt.legend()
plt.show()

#%%

plt.figure()
plt.plot(data.index, data["Water_Temp_Centre_200mm_Avg"], label="Centre_200mm")
plt.plot(data.index, data["Water_Temp_Centre_1000mm_Avg"], label="Centre_1000mm")
plt.plot(data.index, data["Water_Temp_WS_200mm_Avg"], label="WS_200mm")
plt.plot(data.index, data["Water_Temp_WS_1000mm_Avg"], label="WS_1000mm")

plt.plot(data.index, data["Ambient_Temp_FA_Centre_Back_Avg"], label="FA_Centre_Back")

plt.legend()
plt.show()


#%%

plt.figure()
plt.plot(data.index, data["Ambient_Temp_FA_Centre_Avg"], label="FA_Centre")
plt.plot(data.index, data["Ambient_Temp_FA_Centre_Back_Avg"], label="FA_Centre_Back")
plt.plot(data.index, data["Ambient_Temp_WS_Vertical_Avg"], label="WS_Vertical")

plt.legend()
plt.show()

#%%

plt.figure()
plt.plot(data.index, data["Module_Temp_1_Centre_Front_Avg"], label="Centre_Front")
plt.plot(data.index, data["Module_Temp_2_Centre_Left_Avg"], label="Centre_Left")
plt.plot(data.index, data["Module_Temp_3_Centre_Back_Avg"], label="Centre_Back")
plt.plot(data.index, data["Module_Temp_4_FA_Centre_Avg"], label="FA_Centre")
plt.plot(data.index, data["Module_Temp_5_FA_Top_Centre_Avg"], label="FA_Top_Centre")
plt.plot(data.index, data["Module_Temp_6_Centre_Right_Avg"], label="Centre_Right")


plt.legend()
plt.show()


#%%

plt.figure()
plt.plot(data.index, data["Wind_Speed_Avg"], label="Wind_Speed")
plt.plot(data.index, data["Wind_Speed_3s_Max"], label="Wind_Speed_3s_Max")

plt.legend()
plt.show()


#%%

plt.figure()
plt.plot(data.index, data["WD_Avg"], label="WD_Avg")

plt.legend()
plt.show()



#%%


plt.figure()
plt.plot(data.index, data["Relative_Humidity_WS_Vertical_Avg"], label="Relative_Humidity")

plt.legend()
plt.show()

#%% Setting up the target

start_date = "2022-09-21"
end_date = "2022-12-11"

module_temperature_mean = data[['Module_Temp_1_Centre_Front_Avg', 
                                'Module_Temp_2_Centre_Left_Avg',
                                'Module_Temp_3_Centre_Back_Avg', 
                                'Module_Temp_4_FA_Centre_Avg',
                                'Module_Temp_6_Centre_Right_Avg']].mean(axis=1)

target = module_temperature_mean.loc[start_date:end_date]


#%% Setting up the design matrix

X = pd.DataFrame(index=data.index, data=data[["GTI_Avg",
                                               "Ambient_Temp_FA_Centre_Back_Avg",
                                               "Water_Temp_Centre_200mm_Avg",
                                               "Wind_Speed_Avg",
                                               "WD_Avg",
                                               "Relative_Humidity_WS_Vertical_Avg"]])

# Removing times when we have no module temperature measurements
X = X.loc[start_date:end_date]


#%% Making filter for removing NaN values

_nan_filter = X.isna().any(axis=1)

X_filtered = X[~_nan_filter]
target_filtered = target[~_nan_filter]

X_filtered = X_filtered.rename(columns={'GTI_Avg': 'Irradiance', 
                                        'Ambient_Temp_FA_Centre_Back_Avg': 'Air_temperature',
                                        'Water_Temp_Centre_200mm_Avg': 'Water_temperature',
                                        'Wind_Speed_Avg': 'Wind_speed',
                                        'WD_Avg': 'Wind_direction',
                                        'Relative_Humidity_WS_Vertical_Avg': 'Relative_humidity'})

#%% Looking at the correlation matrix for the data

X_and_target = X_filtered
X_and_target["Module_temperature"] = target_filtered

correlation_matrix = X_and_target.corr().round(1)
# use the heatmap function from seaborn to plot the correlation matrix
# annot = True to print the values inside the square
plt.figure(figsize=(15,8))
sns.heatmap(data=correlation_matrix, annot=True)
plt.tight_layout()

plt.show()


#%% Save the data as pickles for easy upload to jupyter notebook

X_and_target.to_pickle(r"C:\Users\vildesn\FYS_STK_4155\Project_3\Project solution\Data.pickle")













