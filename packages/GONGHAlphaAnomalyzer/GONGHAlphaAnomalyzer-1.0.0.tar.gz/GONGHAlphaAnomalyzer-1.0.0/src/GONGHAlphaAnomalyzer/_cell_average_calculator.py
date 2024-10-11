# Copyright (C) 2024  Mahsa Khazaei, Heba Mahdi, Azim Ahmadzadeh

# This file is part of GONG H-Alpha Anomalyzer.
#
# GONG H-Alpha Anomalyzer is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# GONG H-Alpha Anomalyzer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with GONG H-Alpha Anomalyzer. If not, see <https://www.gnu.org/licenses/>.


import os
import cv2
import pandas as pd
import numpy as np
from tqdm import tqdm


def _calculate_cell_average_per_image(image_path, label, grid_size=8):
    """
    Calculate the average pixel value for each cell in a grid for a given 
    image.

    This function reads the image from the specified path in grayscale, 
    divides it into a grid of the given size, and computes the average pixel 
    value for each cell.
    
    Parameters
    ----------
    image_path : str
        The path to the image file.
    label : int
        The label indicating if the image is anomalous (1) or non-anomalous 
        (0).
    grid_size : int, optional
        The number of rows and columns to divide the image into, by default 8.

    Returns
    -------
    image_data : List[List[str, int, int, float, int]]
        A list containing the calculated average pixel values for each grid 
        cell in the image.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    cell_height = height // grid_size
    cell_width = width // grid_size
    image_data = []

    for row in range(grid_size):
        for column in range(grid_size):
            y1, y2 = row * cell_height, (row + 1) * cell_height
            x1, x2 = column * cell_width, (column + 1) * cell_width
            cell = image[y1:y2, x1:x2]
            cell_pixel_avg = np.mean(cell)    
            image_name = os.path.basename(image_path)
            image_data.append([image_name, row, column, cell_pixel_avg, label])

    return image_data

def _calculate_cell_average_per_batch(image_paths, label, grid_size=8, 
                                     desc="Processing Training Images"):
    """
    Process a batch of training images and compute the average pixel value for each cell in each image.

    This function iterates through a list of image paths, processing each 
    image to calculate the average pixel values for its grid cells.

    Parameters
    ----------
    image_paths : List[str]
        A list of paths to the image files.
    label : int
        The label indicating if the images are anomalous (1) or non-anomalous 
        (0).
    grid_size : int, optional
        The number of rows and columns to divide each image into, by default 8.
    desc : str, optional
        Description for the tqdm progress bar, by default "Processing Training 
        Images".

    Returns
    -------
    result_df : pd.DataFrame
        A DataFrame containing the calculated average pixel values for each 
        grid cell in each training image.
    """
    data = []

    for image_path in tqdm(image_paths, desc=desc):
        image_data = _calculate_cell_average_per_image(image_path, label, 
                                                       grid_size)
        data.extend(image_data)

    columns = ['image_name', 'row', 'column', 'cell_pixel_avg', 'label']
    result_df = pd.DataFrame(data, columns=columns)

    return result_df

def _calculate_cell_average(non_anomalous_paths=None, anomalous_paths=None, 
                            grid_size=8):
    """
    Calculate the average pixel value for each cell in a grid for batches of 
    anomalous and/or non-anomalous training images.

    This function processes batches of anomalous and/or non-anomalous image 
    paths, computing the average pixel values for their grid cells.

    Parameters
    ----------
    non_anomalous_paths : List[str], optional
        A list of paths to non-anomalous image files, by default None.
    anomalous_paths : List[str], optional
        A list of paths to anomalous image files, by default None.
    grid_size : int, optional
        The number of rows and columns to divide each image into, by default 8.

    Returns
    -------
    result_df : pd.DataFrame
        A DataFrame containing the calculated average pixel values for each 
        grid cell in the anomalous and/or non-anomalous training image batches.
    """
    non_anomalous_df = pd.DataFrame()
    anomalous_df = pd.DataFrame()

    if non_anomalous_paths:
        non_anomalous_df = _calculate_cell_average_per_batch(
            non_anomalous_paths, 0, grid_size,
            "Processing Non-Anomalous Training Images"
        )
    
    if anomalous_paths:
        anomalous_df = _calculate_cell_average_per_batch(
            anomalous_paths, 1, grid_size,
            "Processing Anomalous Training Images"
        )

    result_df = pd.concat([non_anomalous_df, anomalous_df], ignore_index=True)

    return result_df
