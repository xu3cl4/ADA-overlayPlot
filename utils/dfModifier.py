from datetime import date, datetime

import pandas as pd

ref_1955 = 6.16635504e+10
REFERENCE_DATE = datetime(1955, 1, 1, 0, 0, 0)

points = {
        95 : ["point" + str(num) for num in range(1, 32)],
        110: ["point" + str(num) for num in range(32, 48)]
        }

var_map_sim = {
            'water table': 'depeth to water', 
            'Tritium aqueous concentration': 'tritium', 
            'UO2++ sorbed concentration': 'uranium', 
            'Al+++ aqueous concentration': 'aluminum', 
            'NO3- aqueous concentration': 'nitrate', 
            'pH': 'ph' 
        }

scaling_real = {
            'depth to water': 1, 
            'tritium': 3.22*1.1e-13, 
            'uranium': 1, 
            'aluminum': 1, 
            'nitrate': 1, 
            'ph': 1
        }

def timeStamp2datetime(x: int):
    return datetime.fromtimestamp(x + float(datetime.strptime(str(REFERENCE_DATE), "%Y-%m-%d %H:%M:%S").strftime("%s")))


def modify_df_real(df):
    df['COLLECTION_DATE'] = pd.to_datetime(df['COLLECTION_DATE'])
    for attribute in df.columns: 
        if attribute == 'COLLECTION_DATE': continue 
        df[attribute] = df[attribute]*scaling_real[attribute]

    return df 

def modify_df_sim(df, well):
    # drop the unnecessary data (step1)
    df.columns = ['ob_name', 'region', 'functional', 'variable', 'time', 'value']
    df.drop(['ob_name', 'functional'], axis=1, inplace=True)
    df['region'] = df['region'].str.lstrip()
    df['region'] = df['region'].str.replace(r'Well', 'point')
    df = df[df['region'].isin(points[well])]
    
    df['variable'] = df['variable'].str.lstrip()
    df = df[df['variable'].isin(var_map_sim.keys())]
    
    # make conversions
    df['time'] = df['time'] - ref_1955
    df['time'] = df['time'].apply(timeStamp2datetime)
    df['time'] = pd.to_datetime(df['time'])
    df['variable'] = df['variable'].map(var_map_sim)
     
    # drop the unnecessary data (step2: extract the desired period)
    df = df[(df['time'].dt.year >= 1985) & (df['time'].dt.year <= 2025)]
    
    return df 
