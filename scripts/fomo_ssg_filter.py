# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:00:00 2020

@author: clippeaks
"""

import pandas as pd

def filter_data(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop rows where date conversion failed (NaN values in 'date' column)
    df.dropna(subset=['date'], inplace=True)
    
    return df

if __name__ == "__main__":
    file_path = '/Volumes/KIOXIA/clippeaks/scripts/master_data.csv'
    filtered_df = filter_data(file_path)
    print(filtered_df)