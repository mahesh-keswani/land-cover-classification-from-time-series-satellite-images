
# Land Cover Classification from Time Series Satellite Images

In this project, we try to classify every pixel of the image into a particular land cover class out of 9 classes listed below:

- Urban Areas
- Other built-up surfaces
- Forests
- Sparse Vegetation
- Rocks and bare soil
- Grassland
- Sugarcane crops
- Other crops
- Water

### Dataset

The Dataset can be found in the below link
https://sites.google.com/site/dinoienco/tiselac-time-series-land-cover-classification-challenge

The dataset has been generated from an annual time series of 23 Landsat-8 images acquired in 2014 above the Reunion Island (2866 X 2633 pixels at 30~m spatial resolution), provided at level 2A. Source data have been further processed to fill cloudy observations via pixel-wise multi-temporal linear interpolation on each multi-spectral band (OLI) independently, and compute complementary radiometric indices (NDVI, NDWI and brightness index - BI). A total of 10 features (7 surface reflectances plus 3 indices) are considered for each pixel at each timestamp. 

Reference land cover data has been built using two publicly available dataset, namely the 2012 Corine Land Cover (CLC) map and the 2014 farmers' graphical land parcel registration (Registre Parcellaire Graphique - RPG). The most significant classes for the study area have been retained, and a spatial processing (aided by photo-interpretation) has also been performed to ensure consistency with image geometry. Finally, a pixel-based random sampling of this dataset has been applied to provide an almost balanced ground truth. The final reference training dataset consists of a total of 81714 pixels distributed over 9 classes. 

More in detail, the training dataset is composed by three different files:
- A file containing the pixels values
- A file containing the pixels coordinates w.r.t. the 2866 X 2633 pixels grid
- A file containing the class values
Each file will contain 81714 rows (one for each pixel).

- The first file contains 230 columns (10 features x 23 dates). The columns are temporally ordered, this means that features from 1 to 10 correspond to the first timestamps, features from 11 to 20 correspond to the second timestamps, ..., features from 220 to 230 correspond to the last timestamps. The feature order, for each timestamps, is the same:  7 surface reflectances (Ultra Blue, Blue, Green, Red, NIR, SWIR1 and SWIR2) plus 3 indices (NDVI, NDWI and BI).
- The second file has 2 columns (row, column) of the corresponding pixel time series. This additional information represents the spatial coordinates of the pixel on the image grid. This file contains as many rows as the previous file.
- The third file contains the Land Cover Classes for the training set. The class file contains as many rows as the other files. The value in a row is the class of the corresponding pixel (at the same row) in the other two files.

### Multi Modal CNN for feature extraction

![16](https://user-images.githubusercontent.com/51474076/138552344-fc3c0e29-3b52-44df-bfe6-ddec1d6e8157.png)

**Hyperparameters**
![17](https://user-images.githubusercontent.com/51474076/138552694-cf185c45-8da1-4794-a66d-207fd82e5002.png)

Model Set up:
Here, we first create three 1D CNN models to extract features that may be specific to our three different scale of time series:
- The original time series
- The smoothed time series
- The down sampled time series
They are then concatenated and a new Convolutional layer is added before jumping to 3 fully connected layers. 

The model is quite light in weight ( 921 KB ) but comes with alot of Hyperparameters, making the training relatively harder.

## References
- https://towardsdatascience.com/time-series-land-cover-challenge-a-deep-learning-perspective-6a953368a2bd
- https://sites.google.com/site/dinoienco/tiselac-time-series-land-cover-classification-challenge
