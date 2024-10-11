# Copyright (C) 2024  Mahsa Khazaei, Heba Mahdi, Azim Ahmadzadeh

# This file is part of GONG H-Alpha Anomalyzer.
#
# GONG H-Alpha Anomalyzer is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# GONG H-Alpha Anomalyzer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with GONG H-Alpha Anomalyzer. If not, see <https://www.gnu.org/licenses/>.


import pandas as pd
from scipy.stats import f_oneway
from tqdm import tqdm


def _preprocess_and_filter_data(data_with_ranges):
    """
    Computes the S statistic and separates data by anomaly labels.

    This function calculates the S statistic as the sum of absolute deviations 
    between candidate range values and the average pixel values for each grid 
    cell of the training images data. It then separates the data into two 
    DataFrames based on the anomaly label: one for non-anomalous (label 0) and 
    one for anomalous (label 1) data.

    Parameters
    ----------
    data_with_ranges : pd.DataFrame
        The DataFrame with candidate ranges for each grid cell of the training 
        images data.

    Returns
    -------
    df_label_0 : pd.DataFrame
        A DataFrame with computed S statistics for non-anomalous data (label 
        0).
    df_label_1 : pd.DataFrame
        A DataFrame with computed S statistics for anomalous data (label 1).
    """
    upper_deviation = data_with_ranges['upper_range_val'] - \
                      data_with_ranges['cell_pixel_avg']
    lower_deviation = data_with_ranges['lower_range_val'] - \
                      data_with_ranges['cell_pixel_avg']  
    data_with_ranges['S'] = upper_deviation.abs() + lower_deviation.abs()

    df_label_0 = data_with_ranges[data_with_ranges['label'] == 0]
    df_label_1 = data_with_ranges[data_with_ranges['label'] == 1]
    
    return df_label_0, df_label_1

def _anova_ftest(data_with_ranges, grid_size=8, lower_range_end=20,
                upper_range_start=80, step_size=2):
    """
    Performs One-way ANOVA F-test on S statistics across grid cells and 
    candidate ranges.

    This function calculates the One-way ANOVA F-test statistic between 
    anomalous and non-anomalous images for each combination of grid cell and 
    candidate range of the training images data using the S statistics.

    Parameters
    ----------
    data_with_ranges : pd.DataFrame
        The DataFrame with candidate ranges for each grid cell of the training 
        images data.
    grid_size : int, optional
        The number of rows and columns to divide each image into, by default 8.
    lower_range_end : int, optional
        The end of candidate lower ranges, by default 20.
    upper_range_start : int, optional
        The start of candidate upper ranges, by default 80.
    step_size : int, optional
        The step size for candidate ranges, by default 2.

    Returns
    -------
    df_anova_results : pd.DataFrame
        A DataFrame with computed F-statistic for each combination of grid 
        cell and candidate range of the training images data.
    """
    df_label_0, df_label_1 = _preprocess_and_filter_data(data_with_ranges)

    results = []

    for row in tqdm(range(grid_size), desc="Performing One-way ANOVA F-test"):
        for column in range(grid_size):
            for lower_range in range(0, lower_range_end, step_size):
                for upper_range in range(upper_range_start, 100, step_size):

                    subset_label_0 = df_label_0[
                        (df_label_0['row'] == row) &
                        (df_label_0['column'] == column) &
                        (df_label_0['lower_range'] == lower_range) &
                        (df_label_0['upper_range'] == upper_range)
                    ]
                    
                    subset_label_1 = df_label_1[
                        (df_label_1['row'] == row) &
                        (df_label_1['column'] == column) &
                        (df_label_1['lower_range'] == lower_range) &
                        (df_label_1['upper_range'] == upper_range)
                    ]
                    
                    data_label_0 = subset_label_0['S'].values
                    data_label_1 = subset_label_1['S'].values

                    f_statistic, _ = f_oneway(*[data_label_0, 
                                                    data_label_1])

                    results.append([
                        row, column, lower_range, upper_range,
                        subset_label_0['lower_range_val'].values[0],
                        subset_label_0['upper_range_val'].values[0],
                        f_statistic
                    ])

    columns = [
        'row', 'column', 'lower_range', 'upper_range',
        'lower_range_val', 'upper_range_val', 'f_statistic'
    ]
    df_anova_results = pd.DataFrame(results, columns=columns)

    return df_anova_results
