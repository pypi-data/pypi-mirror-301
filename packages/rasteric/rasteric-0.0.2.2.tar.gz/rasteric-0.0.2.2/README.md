
# Rasteric: A Comprehensive Geospatial Library

**Rasteric** is a comprehensive library for geospatial data preprocessing, analysis, and modeling. It provides a variety of functions for transforming and manipulating geospatial data, including:

- Data normalization with `norm()`
- Resampling using `resample()`
- Feature extraction through `extract()`

It also offers analytical techniques such as:

- `zonalstats()` for spatial analysis
- `ndvi()` for vegetation index calculation
- `haversine()` for distance calculations

## Supported Data Formats

Rasteric is designed to work with multiple geospatial data formats, including:

- Shapefiles
- GeoJSON
- Raster data

## Key Functions

### Data Handling
- `convpath()` for file path handling
- `stack_rasters()` for combining multiple rasters
- `convras()` for converting rasters to vector format

### Visualization
- `plot()` for displaying raster data
- `contour()` for creating contour plots
- `hist()` for histogram generation

### Data Manipulation
- `clipraster()` for cropping rasters
- `reproject_raster()` for coordinate system transformations
- `bandnames()` for managing raster band information

### Utilities
- `mergecsv()` for combining data files
- `savetif()` for saving processed data

## Integration and Applications

Rasteric integrates seamlessly with popular geospatial tools and platforms, enhancing its functionality with features like:

- `getFeatures()` for working with vector data
- `stats()` for quick raster statistics

Widely used in the geospatial industry, research, and open-source communities, Rasteric facilitates:

- Development of geospatial applications
- Performance of spatial analysis
- Modeling of complex geospatial phenomena

Its diverse set of functions, including `zonalstats()`, `ndvi()`, and `resample()`, make it a versatile tool for a wide range of geospatial tasks.

## Example:

```python
from rasteric import raster
from matplotlib import pyplot

fig, (axr, axg, axb) = pyplot.subplots(1, 3, figsize=(21, 7))

fig, (axr, axg, axb) = pyplot.subplots(1, 3, figsize=(21, 7))

raster.plot('T60GVV.tif', bands=[3], ax=axr, title="Red", brightness_factor=5)
raster.plot('IMG_001_clip.tif', bands=[4,2,1], ax=axg, title="Green", brightness_factor=5)
raster.plot('IMG_001_clip.tif', bands=[4], ax=axb, title="Red")

```

![Example Image](https://github.com/tnmthai/geotran/blob/main/image.png)
```python
clip(raster_file, shapefile, output_file)
```

---

## Function Descriptions
### convpath(file_path)
Converts a Windows-style file path to a Unix-style path for cross-platform compatibility.

**Parameters:**
- `file_path` (str): The input file path to be converted.

---

### norm(array)
Applies min-max normalization to a raster array, adjusting pixel values between 0 and 1.

**Parameters:**
- `array` (numpy array): The input raster array to be normalized.

---

### plot(file, bands=(3, 2, 1), cmap='viridis', title='Raster photo', ax=None)
Displays a raster image using specified bands, allowing visualization of multi-band or single-band images.

**Parameters:**
- `file` (str): Path to the raster file.
- `bands` (tuple): Bands to be displayed (default is (3, 2, 1) for RGB).
- `cmap` (str): Colormap to be used (default is 'viridis').
- `title` (str): Title for the plot (default is 'Raster photo').
- `ax` (matplotlib.axes.Axes): Optional axes object to plot on.

---

### contour(file)
Plots a raster image with overlaid contours to visualize elevation changes or continuous data variations.

**Parameters:**
- `file` (str): Path to the raster file.

---

### hist(file, bin=50, title="Histogram")
Plots a histogram of raster values to display the distribution of pixel intensities.

**Parameters:**
- `file` (str): Path to the raster file.
- `bin` (int): Number of bins for the histogram (default is 50).
- `title` (str): Title for the histogram plot (default is "Histogram").

---

### haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float
Calculates the great-circle distance between two geographical points using latitude and longitude.

**Parameters:**
- `lon1` (float): Longitude of the first point.
- `lat1` (float): Latitude of the first point.
- `lon2` (float): Longitude of the second point.
- `lat2` (float): Latitude of the second point.

**Returns:**
- float: The distance between the two points in kilometers.

---

### stack(input_files, output_file, band_names=None)
Stacks multiple raster files into a single multi-band raster file.

**Parameters:**
- `input_files` (list): List of paths to input raster files.
- `output_file` (str): Path to the output stacked raster file.
- `band_names` (list): Optional list of names for the output bands.

---

### bandnames(input_raster, band_names)
Updates the names of bands in a raster file to provide meaningful descriptions.

**Parameters:**
- `input_raster` (str): Path to the input raster file.
- `band_names` (list): List of new names for the raster bands.

---

### getFeatures(geo)
Retrieves geometric features from a given geographical input.

**Parameters:**
- `geo` (GeoDataFrame): Input GeoDataFrame containing the geometries.

---

### clip(raster_file, shapefile, output_file, epsg_code=4326)
Clips a raster file using a shapefile polygon and exports the result to a new raster file.

**Parameters:**
- `raster_file` (str): Path to the input raster file.
- `shapefile` (str): Path to the shapefile used for clipping.
- `output_file` (str): Path to the output clipped raster file.
- `epsg_code` (int): EPSG code for the output raster (default is 4326).

---

### extract(rf, shp, all_touched=False)
Extracts pixel values from a raster based on geometries in a shapefile, storing results in a GeoDataFrame.

**Parameters:**
- `rf` (str): Path to the raster file.
- `shp` (str): Path to the shapefile.
- `all_touched` (bool): If True, include all pixels touched by geometries (default is False).

---

### savetif(output, gdf, colname='FVC', input_raster=None, resolution=10, dtype=rasterio.float32)
Converts vector data into a raster file and burns values from a GeoDataFrame column into the raster.

**Parameters:**
- `output` (str): Path to the output raster file.
- `gdf` (GeoDataFrame): Input GeoDataFrame containing geometries and values.
- `colname` (str): Column name in the GeoDataFrame to use for raster values (default is 'FVC').
- `input_raster` (str): Optional path to an input raster for reference.
- `resolution` (int): Desired resolution for the output raster (default is 10).
- `dtype`: Data type for the output raster (default is rasterio.float32).

---

### mergecsv(path, outfile='combined_all.csv')
Combines multiple CSV files from a specified directory into a single CSV file.

**Parameters:**
- `path` (str): Path to the directory containing CSV files.
- `outfile` (str): Name of the output merged CSV file (default is 'combined_all.csv').

---

### reproject(input_raster, output_raster, target_crs)
Reprojects a raster to a different coordinate reference system (CRS).

**Parameters:**
- `input_raster` (str): Path to the input raster file.
- `output_raster` (str): Path to the output reprojected raster file.
- `target_crs`: Target coordinate reference system.

---

### ndvi(red_band, nir_band)
Calculates the Normalized Difference Vegetation Index (NDVI) from red and near-infrared bands.

**Parameters:**
- `red_band` (numpy array): The red band values.
- `nir_band` (numpy array): The NIR band values.

---

### zonalstats(raster_file, vector_file, stats=['mean', 'max', 'min', 'std'])
Calculates zonal statistics for each polygon in a vector file based on underlying raster values.

**Parameters:**
- `raster_file` (str): Path to the input raster file.
- `vector_file` (str): Path to the input vector file.
- `stats` (list): List of statistics to calculate (default is ['mean', 'max', 'min', 'std']).

---

### convras(raster_file, output_shapefile, field_name='value')
Converts a raster to a vector format (polygons).

**Parameters:**
- `raster_file` (str): Path to the input raster file.
- `output_shapefile` (str): Path to the output shapefile.
- `field_name` (str): Name of the field to store raster values (default is 'value').

---

### resample(input_raster, output_raster, scale_factor=2, resampling_method='bilinear')
Resamples a raster to a different resolution using a specified scale factor and resampling method.

**Parameters:**
- `input_raster` (str): Path to the input raster file.
- `output_raster` (str): Path to the output resampled raster file.
- `scale_factor` (float): Scale factor for resampling (default is 2).
- `resampling_method` (str): Resampling method to use (default is 'bilinear').

---

### stats(raster_file)
Calculates basic statistics (min, max, mean, std) for a raster file.

**Parameters:**
- `raster_file` (str): Path to the input raster file.

---