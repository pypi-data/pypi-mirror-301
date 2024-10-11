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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import Normalize, to_rgba
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tqdm import tqdm
from PIL import Image
from typing import List, Tuple
from ._cell_average_calculator import _calculate_cell_average
from ._anova_analysis import _anova_ftest
from ._cell_range_calculator import _calculate_cell_wise_ranges

class Anomalyzer:
    """
    A class for detecting anomalies in full-disk H-Alpha solar observations by 
    superimposing a grid, computing average pixel values per grid cell, and 
    performing statistical analysis to determine the best normal range values 
    per grid cell.

    Attributes
    ----------
    grid_size : int
        The number of rows and columns to divide each image into.
    best_ranges : pd.DataFrame
        The DataFrame containing the best range values for each grid cell.
    images_data : pd.DataFrame
        The DataFrame containing the training images data.
    mean : pd.DataFrame
        The DataFrame containing the mean S statistic values for each grid 
        cell.
    std : pd.DataFrame
        The DataFrame containing the standard deviation of S statistic values 
        for each grid cell.
    """
    def __init__(self, grid_size: int = 8):
        """
        Initializes the Anomalyzer with a specified grid size.

        Parameters
        ----------
        grid_size : int, optional
            The number of rows and columns to divide each image into, by 
            default 8.
        """
        self.grid_size = grid_size
        self.best_ranges: pd.DataFrame = pd.DataFrame()
        self.images_data: pd.DataFrame = pd.DataFrame()
        self.mean: pd.DataFrame = pd.DataFrame()
        self.std: pd.DataFrame = pd.DataFrame()

    def _process_image(self, image_path: str) \
            -> List[Tuple[int, int, float, float]]:
        """
        Processes an image to calculate the average pixel and S statistic 
        values for each cell in a grid for a given image.

        This function reads the image from the specified path in grayscale, 
        divides it into a grid of cells, and computes the average pixel value 
        for each cell. It calculates the S statistic as the sum of absolute 
        deviations between best range values and the average pixel values for 
        each cell.

        Parameters
        ----------
        image_path : str
            The path to the image file.

        Returns
        -------
        image_data : List[Tuple[int, int, float, float]]
            A list containing the calculated average pixel and S statistic 
            values for each grid cell in the image.
        """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        height, width = image.shape
        cell_height = height // self.grid_size
        cell_width = width // self.grid_size

        image_data = []
        for row in range(self.grid_size):
            for column in range(self.grid_size):
                y1, y2 = row * cell_height, (row + 1) * cell_height
                x1, x2 = column * cell_width, (column + 1) * cell_width
                cell = image[y1:y2, x1:x2]
                cell_pixel_avg = np.mean(cell)

                best_upper_range_val = self.best_ranges.loc[
                    (self.best_ranges['row'] == row) &
                    (self.best_ranges['column'] == column),
                    'best_upper_range_val'
                ].values[0]

                best_lower_range_val = self.best_ranges.loc[
                    (self.best_ranges['row'] == row) &
                    (self.best_ranges['column'] == column),
                    'best_lower_range_val'
                ].values[0]

                upper_deviation = best_upper_range_val - cell_pixel_avg
                lower_deviation = best_lower_range_val - cell_pixel_avg
                S = abs(upper_deviation) + abs(lower_deviation)

                image_data.append((row, column, cell_pixel_avg, S))

        return image_data

    def _compute_stats(self) -> None:
        """
        Computes mean and standard deviation of S statistic values for each 
        grid cell of the training images data.
        """
        all_data = []
        for _, row in tqdm(self.images_data.iterrows(), 
                           total=len(self.images_data), 
                           desc="Computing Statistics"):
            best_upper_range_val = self.best_ranges.loc[
                (self.best_ranges['row'] == row['row']) & 
                (self.best_ranges['column'] == row['column']), 
                'best_upper_range_val'].values[0]

            best_lower_range_val = self.best_ranges.loc[
                (self.best_ranges['row'] == row['row']) & 
                (self.best_ranges['column'] == row['column']), 
                'best_lower_range_val'].values[0]

            S = abs(best_upper_range_val - row['cell_pixel_avg']) + abs(best_lower_range_val - row['cell_pixel_avg'])

            all_data.append({
                'image_name': row['image_name'],
                'row': row['row'],
                'column': row['column'],
                'S': S
            })

        df = pd.DataFrame(all_data, columns=['image_name', 'row', 'column', 'S'])

        grouped_df = df.groupby(['row', 'column'])['S'].agg(['mean', 'std'])\
            .reset_index()

        self.mean = grouped_df[['row', 'column', 'mean']]
        self.std = grouped_df[['row', 'column', 'std']]
 
    def _compute_anomaly_likelihoods(self, 
                                    image_paths: List[str]) -> pd.DataFrame:
        """
        Computes the anomaly likelihood (standardized sigmoid of S statistic) 
        of each grid cell of the test images.

        This function processes a list of image paths to calculate the S 
        statistic for each grid cell. The S statistic is then standardized and 
        transformed using a sigmoid function to produce an anomaly likelihood 
        for each cell.

        Parameters
        ----------
        image_paths : List[str]
            The list of paths to the image files.

        Returns
        -------
        df_anomaly_likelihoods : pd.DataFrame
            A DataFrame containing the calculated anomaly likelihoods of each 
            grid cell of the test images.
        """
        data = []

        for image_path in tqdm(image_paths, 
                               desc="Computing Anomaly Likelihoods"):
            image_data = self._process_image(image_path)
            image_name = os.path.basename(image_path)

            for row, column, cell_pixel_avg, S in image_data:
                mean = self.mean.loc[
                    (self.mean['row'] == row) & 
                    (self.mean['column'] == column), 'mean'].values[0]
                std = self.std.loc[
                    (self.std['row'] == row) & 
                    (self.std['column'] == column), 'std'].values[0]

                standardized_S = (S - mean) / std
                standardized_S = np.where(np.isnan(standardized_S), 
                                          -np.inf, standardized_S)
                standardized_S_Sigmoid = 1 / (1 + np.exp(-standardized_S))
                data.append([image_name, image_path, row, column, 
                             cell_pixel_avg, standardized_S_Sigmoid])

        df_anomaly_likelihoods = pd.DataFrame(data, columns=[
            'image_name', 'image_path', 'row', 'column', 
            'cell_pixel_avg', 'standardized_S_Sigmoid'
        ])

        return df_anomaly_likelihoods
       
    def compute_best_ranges(self,
                            non_anomalous_paths: List[str] = None,
                            anomalous_paths: List[str] = None,
                            lower_range_end: int = 20,
                            upper_range_start: int = 80,
                            step_size: int = 2) -> None:
        """
        Compute the best range values for each grid cell based on the highest 
        One-way ANOVA F-test statistic.

        Parameters
        ----------
        non_anomalous_paths : List[str], optional
            A list of paths to non-anomalous image files.
        anomalous_paths : List[str], optional
            A list of paths to anomalous image files.
        lower_range_end : int, optional
            The end of candidate lower ranges, by default 20.
        upper_range_start : int, optional
            The start of candidate upper ranges, by default 80.
        step_size : int, optional
            The step size for candidate ranges, by default 2.

        Notes
        -----
        - Users must provide both lists of paths to the anomalous and 
        non-anomalous image files for training; an error is raised if the 
        lists are not provided.
        - The images should be H-alpha GONG solar observations in JPG, JPEG, 
        or PNG format.
        - Users can optionally set the `lower_range_end`, 
        `upper_range_start`, and `step_size` parameters:
            - These parameters are used by the One-way ANOVA F-test to rank 
            the best range that differentiates between normal and anomalous 
            images for each cell.
            - The lower range candidates will start from 0 and end at  
            `lower_range_end` minus `step_size`. For example, if  
            `lower_range_end` is set to 20 and `step_size` is 2, the lower 
            range candidates will start from 0 and end at 18 with a step size 
            of 2; the lower range percentage candidates are 0, 2, 4, 6, ...,18.
            - The upper range candidates will start from `upper_range_start` 
            and end at 100 minus `step_size`. For example, if 
            `upper_range_start` is set to 80 and `step_size` is 2, the upper 
            range candidates will start from 80 and end at 98 with a step size 
            of 2; the upper range percentage candidates are 80, 82, 84,  
            86, ..., 98.
        """
        if not non_anomalous_paths or not anomalous_paths:
            raise ValueError("Both non-anomalous and anomalous paths must be \
                             provided.")
        self.images_data = _calculate_cell_average(non_anomalous_paths, 
                                        anomalous_paths, self.grid_size) 
        data_with_ranges = _calculate_cell_wise_ranges(self.images_data, 
                                                       self.grid_size, 
                                                       lower_range_end, 
                                                       upper_range_start, 
                                                       step_size)
        anova_results = _anova_ftest(data_with_ranges, self.grid_size, 
                                     lower_range_end, upper_range_start, 
                                     step_size)
        anova_results['f_statistic'] = anova_results['f_statistic'].fillna(-1)

        results = []

        for row in tqdm(range(self.grid_size), 
                        desc="Computing Best Ranges Using ANOVA"):
            for column in range(self.grid_size):
                cell_data = anova_results[
                    (anova_results['row'] == row) & 
                    (anova_results['column'] == column)
                ]
                if not cell_data.empty:
                    best_range = \
                    cell_data.loc[cell_data['f_statistic'].idxmax()]
                    results.append([row, column, 
                                    best_range['lower_range_val'], 
                                    best_range['upper_range_val']])

        columns = ['row', 'column', 'best_lower_range_val', 
                   'best_upper_range_val']
        self.best_ranges = pd.DataFrame(results, columns=columns)

        self._compute_stats()

    def find_corrupt_images(self,
                            image_paths: List[str] = None,
                            likelihood_threshold: float = 0.5,
                            min_corrupt_cells: int = 0,
                            verbose: bool = False) -> List[int]:
        """
        Identifies corrupt images based on the anomaly likelihood of grid 
        cells.

        This function evaluates each image based on the anomaly likelihoods of 
        its grid cells. An image is marked as corrupt if the number of grid 
        cells exceeding the likelihood threshold is greater than the specified 
        minimum number of corrupt cells.

        Parameters
        ----------
        image_paths : List[str]
            The list of paths to the image files.
        likelihood_threshold : float, optional
            The threshold for the anomaly likelihood to consider a cell as 
            corrupt, by default 0.5.
        min_corrupt_cells : int, optional
            The minimum number of corrupt cells required to classify an image 
            corrupt, by default 0.
        verbose : bool, optional
            If True, prints the number of corrupt images detected, by default 
            False.

        Returns
        -------
        anomaly_labels : List[int]
            List of binary labels where 0 indicates a non-corrupt image and 1 
            indicates a corrupt image.

        Notes
        -----
        - Users must provide a list of paths to the image files for testing.
        - The images should be H-alpha GONG solar observations in JPG, JPEG, 
        or PNG format.
        """
        anomaly_labels = []

        image_data = self._compute_anomaly_likelihoods(image_paths)
        image_data['label'] = image_data['standardized_S_Sigmoid'].apply(
            lambda x: 1 if x > likelihood_threshold else 0
        )

        for image_path in tqdm(image_paths, desc="Detecting Corrupt Images"):
            image_name = os.path.basename(image_path)
            group = image_data[image_data['image_name'] == image_name]
            
            if group['label'].astype(int).sum() > min_corrupt_cells:
                anomaly_labels.append(1)
            else:
                anomaly_labels.append(0)

        if verbose:
            print("Number of corrupt images detected: " + 
                str(anomaly_labels.count(1)))

        return anomaly_labels

    def plot_image_likelihoods(self, image_path: str = None, 
                            likelihood_threshold: float = None) -> None:
        """
        Plots the original image alongside the processed image with grid cell 
        anomaly likelihoods indicated by a colormap. Optionally outlines 
        corrupt cells based on a specified likelihood threshold.

        Parameters
        ----------
        image_path : str
            The path to the image file.
        likelihood_threshold : float, optional
            The likelihood threshold for identifying corrupt cells, by default 
            None.
        
        Notes
        -----
        - Users must provide a paths to the image file for plotting.
        - The image should be H-alpha GONG solar observation in JPG, JPEG, 
        or PNG format.
        """
        img = Image.open(image_path)
        width, height = img.size
        cell_width = width // self.grid_size
        cell_height = height // self.grid_size

        fig, axs = plt.subplots(1, 2, figsize=(18, 6), facecolor='black', gridspec_kw={'width_ratios': [1, 1], 'wspace': -0.45})

        ax1, ax2 = axs

        img_resized = img.resize((width, height))

        ax1.imshow(img_resized, cmap='gray')
        ax1.set_xticks(np.arange(0, width, cell_width))
        ax1.set_yticks(np.arange(0, height, cell_height))
        ax1.grid(which='both', color='purple', linestyle='-', linewidth=1)
        ax1.set_title('Original Image', color='white', fontsize=16)

        ax2.imshow(img, cmap='gray')

        scalar_map = ScalarMappable(norm=Normalize(vmin=0, vmax=1), 
                                    cmap='Purples')

        df_anomaly_likelihoods = \
        self._compute_anomaly_likelihoods([image_path])

        for _, row in df_anomaly_likelihoods.iterrows():
            row_idx = row['row']
            col_idx = row['column']
            standardized_S_Sigmoid = row['standardized_S_Sigmoid']

            x, y = col_idx * cell_width, row_idx * cell_height
            color = scalar_map.to_rgba(standardized_S_Sigmoid, alpha=0.5)

            if likelihood_threshold is not None \
            and standardized_S_Sigmoid > likelihood_threshold:
                edge_color = to_rgba('red', alpha=1)
                linewidth = 2
            else:
                edge_color = to_rgba('purple', alpha=1)
                linewidth = 0.75

            rect = patches.Rectangle((x, y), cell_width, cell_height,
                                    linewidth=linewidth, facecolor=color,
                                    edgecolor=edge_color)
            ax2.add_patch(rect)

            if likelihood_threshold is not None and standardized_S_Sigmoid > likelihood_threshold:
                ax2.text(x + cell_width / 2, y + cell_height / 2,
                        f'{standardized_S_Sigmoid:.2f}', color='white',
                        ha='center', va='center', fontsize=12)

        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.grid(which='both', color='purple', linestyle='-', linewidth=1)
        ax2.set_title('Image with Anomaly Likelihoods', 
                      color='white', fontsize=16)

        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = fig.colorbar(scalar_map, cax=cax, 
                            orientation='vertical', 
                            ticks=np.arange(0, 1.1, 0.1))
        cbar.set_label('Sigmoid of Standardized S values', 
                       color='white', fontsize=14)
        cbar.ax.tick_params(labelsize=12)
        for label in cbar.ax.get_yticklabels():
            label.set_color('white')
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

        if likelihood_threshold is not None:
            threshold_norm = Normalize(vmin=0, vmax=1)(likelihood_threshold)
            cbar.ax.axhline(y=threshold_norm, color='red', linewidth=2)
            cbar.ax.text(0.5, threshold_norm - 0.1, f'Threshold: {likelihood_threshold:.2f}',
                        color='red', ha='center', va='center', rotation=90,
                        transform=cbar.ax.get_yaxis_transform())

        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, 
                            wspace=0, hspace=0)
        plt.show()
        
