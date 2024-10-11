# GONGHAlphaAnomalyzer

_(Part of the [MLEcoFi Project](https://www.mlecofi.net/))_

**GONGHAlphaAnomalyzer** is a software for detecting anomalies in GONG H-Alpha full-disk solar observations. Leveraging a grid-based approach and advanced statistical analysis, it computes optimal pixel average range values for each grid cell to identify anomalies effectively.

[![PyPI - Version](https://img.shields.io/pypi/v/GONGHAlphaAnomalyzer)](https://pypi.org/project/GONGHAlphaAnomalyzer/)
[![Read the Docs](https://img.shields.io/readthedocs/gonghalphaanomalyzer)](https://gonghalphaanomalyzer.readthedocs.io/en/latest/)
[![PyPI - License](https://img.shields.io/pypi/l/GONGHAlphaAnomalyzer)](https://opensource.org/license/gpl-3-0)

Try the demo online

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fbitbucket.org%2Fdataresearchlab%2Fgonghalphaanomalyzer/deployment?urlpath=lab/tree/binder)

## Table of Contents

- [Installation](#installation)
- [Importing Required Library](#importing-required-library)
- [Initializing Anomalyzer](#initializing-anomalyzer)
- [Computing Best Ranges](#computing-best-ranges)
- [Finding Corrupt Images](#finding-corrupt-images)
- [Plotting Image Likelihoods with Corrupt Cells](#plotting-image-likelihoods-with-corrupt-cells)
- [Example Outputs](#example-outputs)

## User Manual

### Installation

To install the required library, run:

```bash
pip install GONGHAlphaAnomalyzer
```

### Importing Required Class

Import the Anomalyzer class from the library's anomalyzer module into your Python script with:

```python
from GONGHAlphaAnomalyzer.anomalyzer import Anomalyzer
```

### Initializing Anomalyzer Object

Create an instance of `Anomalyzer` with a specified grid size:

```python
anomalyzer = Anomalyzer(grid_size=8)
```

### Computing Best Ranges

Calculate optimal range values for each grid cell using your image paths.

```python
anomalyzer.compute_best_ranges(
    non_anomalous_paths=['path/to/non-anomalous/image1.png', 'path/to/non-anomalous/image2.png'],
    anomalous_paths=['path/to/anomalous/image1.png', 'path/to/anomalous/image2.png']
)
```

**Parameters:**

1. `non_anomalous_paths`: List of paths to non-anomalous image files.
2. `anomalous_paths`: List of paths to anomalous image files.
3. `lower_range_end`: End of candidate lower ranges, default is 20.
4. `upper_range_start`: Start of candidate upper ranges, default is 80.
5. `step_size`: Step size for candidate ranges, default is 2.

### Finding Corrupt Images

Detect corrupt images based on computed best ranges, with options to set likelihood thresholds and minimum corrupt cells:

```python
corrupt_images_labels = anomalyzer.find_corrupt_images(
    image_paths=['path/to/image1.png', 'path/to/image2.png'],
    likelihood_threshold=0.6,
    min_corrupt_cells=1,
    verbose=True
)
```

**Parameters:**

1. `image_paths`: List of paths to image files.
2. `likelihood_threshold`: Threshold for considering a cell as corrupt, default is 0.5.
3. `min_corrupt_cells`: Minimum number of corrupt cells required to classify an image as corrupt, default is 0.
4. `verbose`: If True, prints the number of detected corrupt images, default is False.

### Plotting Image Likelihoods with Corrupt Cells

Visualize the anomaly likelihoods with an option to highlight corrupt cells:

```python
anomalyzer.plot_image_likelihoods(
    image_path='path/to/image.png',
    likelihood_threshold=0.6
)
```

**Parameters:**

1. `image_path`: Path to the image file.
2. `likelihood_threshold`: Optional threshold for identifying corrupt cells. If provided, corrupt cells will be outlined.

### Example Outputs


![Anomaly_Likelihoods_With Threshold](https://bitbucket.org/dataresearchlab/gonghalphaanomalyzer/raw/334e18c4ba7cdad41115714d605811261e552389/_readme_images/20130114105034Ch_Anomaly_Likelihoods.jpeg)

