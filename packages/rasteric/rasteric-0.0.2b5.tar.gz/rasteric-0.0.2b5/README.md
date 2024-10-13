
# Rasteric - Python Geospatial Library

**Rasteric** is a comprehensive toolkit for geospatial data preprocessing, analysis, and modeling. It provides a variety of functions for transforming and manipulating geospatial data, including data normalization, resampling, filtering, and feature extraction. It also offers a range of analytical techniques, such as spatial clustering, classification, and regression, as well as machine learning algorithms for predictive modeling.

Rasteric is designed to work with multiple geospatial data formats, including shapefiles, GeoJSON, and raster data. It integrates seamlessly with popular geospatial tools and platforms such as QGIS, GDAL, and ArcGIS.

Rasteric is widely used in the geospatial industry, research, and open-source communities for developing geospatial applications, performing spatial analysis, and modeling complex geospatial phenomena.

## Example:

```python
from rasteric import raster
from matplotlib import pyplot

fig, (axr, axg, axb) = pyplot.subplots(1, 3, figsize=(21, 7))

raster.plot('T60GVV.tif', bands=[3], ax=axr, title="Red", cmap='Reds')
raster.plot('T60GVV.tif', bands=[2], ax=axg, title="Green", cmap="Greens")
raster.plot('T60GVV.tif', bands=[1], ax=axb, title="Blue", cmap="Blues")
```

![Alt text](image.png)

```python
clip_raster_by_shp(raster_file, shapefile, output_file, epsg_code=2193)
```

---

## Function Descriptions

### `convert_path(file_path)`
Converts a Windows-style file path (with backslashes) to a Unix-style path (with forward slashes) for cross-platform compatibility.

**Usage**:  
Converts a path like `"C:\Program Files\Example"` to `"C:/Program Files/Example"`.

### `normalise(array)`
Applies min-max normalization to a raster array. This function adjusts pixel values so they fall between 0 and 1 based on the 0.5th and 99.5th percentiles.

**Usage**:  
Useful for normalizing pixel values for visualization or comparison between images.

### `plot(file, bands=(3, 2, 1), cmap='viridis', title='Raster photo', ax=None)`
Displays a raster image using the specified bands. It can plot a 3-band composite image (e.g., RGB) or a single band for grayscale images.

**Usage**:  
Visualize different bands of a satellite image or raster data with an optional colormap (`cmap`).

### `plot_contour(file)`
Plots a raster image with overlaid contours. Contours help visualize elevation changes or other continuous data across a surface.

**Usage**:  
Helps to better understand the topography or intensity variation in your raster data.

### `plot_hist(file, bin=50, title="Histogram")`
Plots a histogram of the raster values to display the distribution of pixel intensities. You can adjust the number of bins.

**Usage**:  
Ideal for analyzing the distribution of pixel values in a raster and spotting outliers or areas of interest.

### `haversine(lon1, lat1, lon2, lat2)`
Calculates the great-circle distance between two geographical points using their latitude and longitude.

**Usage**:  
Determine the distance (in kilometers) between two locations on Earth.

### `stack_rasters(input_files, output_file, band_names=None)`
Stacks multiple raster files into a single multi-band raster. The band names can be updated to reflect the contents.

**Usage**:  
Combine several single-band raster images (e.g., one for each color channel) into one multi-band raster file.

### `update_band_names(input_raster, band_names)`
Updates the names of bands in a raster file.

**Usage**:  
Modify metadata to provide meaningful descriptions for the raster bands (e.g., `Red`, `Green`, `Blue`).

### `clip_raster_by_shp(raster_file, shapefile, output_file, epsg_code=4326)`
Clips a raster file using a shapefile polygon and exports the result to a new raster file.

**Usage**:  
Extract a region of interest from a larger raster dataset using a vector geometry (shapefile).

### `extract(rf, shp, all_touched=False)`
Extracts pixel values from a raster file based on the geometries in a shapefile and stores the results in a GeoDataFrame.

**Usage**:  
Perform zonal statistics, associating raster data (e.g., elevation, temperature) with specific polygons from a shapefile.

### `savetif(output, gdf, colname='FVC', input_raster=None, resolution=10, dtype=rasterio.float32)`
Converts vector data into a raster file and burns values from a GeoDataFrame column into the raster.

**Usage**:  
Rasterize vector data, such as converting land cover types or vegetation indices into a raster format for analysis.

### `combine_csv_files(path, outfile='combined_all.csv')`
Combines multiple CSV files from a specified directory into a single CSV file.

**Usage**:  
Useful for merging data from multiple sources, such as sensor outputs or regional analysis results, into one file for further processing.
