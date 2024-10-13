from math import radians, cos, sin, asin, sqrt
import rasterio
from matplotlib import pyplot
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
import pandas as pd
import shutil
from rasterio.warp import reproject, Resampling, calculate_default_transform
from shapely.geometry import Point
from rasterio import transform
from rasterio import features
from rasterio.enums import MergeAlg
import os
from glob import glob
from rasterstats import zonal_stats

def convpath(file_path):
    """
    Converts a given file path string to a raw string and replaces backslashes with forward slashes.

    Parameters:
    - file_path (str): The original file path string with potential backslashes.

    How it works:
    1. **Convert the string to a raw string**: 
        - The input file path is formatted using `r"{}".format(file_path)`. This treats backslashes as literal characters rather than escape sequences, ensuring that the path is properly interpreted.
    
    2. **Replace backslashes with forward slashes**: 
        - The function uses `file_path.replace("\\", "/")` to convert all backslashes (`\`) in the file path to forward slashes (`/`). This is especially useful for ensuring compatibility across different operating systems, like converting Windows-style paths (`C:\...`) to Unix-style paths (`C:/...`).
    
    3. **Return the modified file path**: 
        - The function returns the path after converting backslashes to forward slashes.

    Example usage:
    new_path = convpath("C:\\Program Files\\Double Commander\\pixmaps")
    """
    # Convert the string to a raw string (add 'r' before the string)
    file_path = r"{}".format(file_path)
    
    # Replace backslashes with forward slashes
    file_path = file_path.replace("\\", "/")
    
    return file_path

def normalize(data):
    """
    Normalize the input data to the range [0, 1].
    """
    min_val = np.min(data)
    max_val = np.max(data)
    return (data - min_val) / (max_val - min_val)
 
def norm(array):
    """
    Normalizes a given NumPy array to a range between 0 and 1 based on its percentiles.

    Parameters:
    - array (numpy.ndarray): The input array to be normalized.

    How it works:
    1. **Calculate the minimum and maximum**:
        - The function computes the 0.5th percentile as the minimum value and the 99.5th percentile as the maximum value of the input array. This helps to mitigate the influence of outliers on the normalization process.
    
    2. **Normalize the array**:
        - The normalization formula `(array - min) / (max - min)` is applied to scale the values of the array between 0 and 1. Values below the minimum percentile will be set to 0, and values above the maximum percentile will be set to 1.
    
    3. **Clamp values**:
        - The normalized values are clamped to ensure they remain within the range of 0 to 1. Any value in the normalized array that is less than 0 is set to 0, and any value greater than 1 is set to 1.

    4. **Return the normalized array**:
        - The function returns the normalized array.

    Example usage:
    normalized_array = norm(np.array([1, 2, 3, 4, 5, 100]))
    """
    min = np.percentile(array, 0.5)  
    max = np.percentile(array, 99.5)    
    norm = (array - min) / (max - min)
    norm[norm < 0.0] = 0.0
    norm[norm > 1.0] = 1.0
    return norm

def brighten(image, brightness_factor):
    """Brighten the normalized image by scaling pixel values."""
    brightened_image = np.clip(image * brightness_factor, 0, 1)  # Clip to [0, 1]
    return brightened_image

def plot(file, bands=(3, 2, 1), cmap='viridis', title='Raster photo', ax=None, brightness_factor=4):
    """
    Plots a raster image using specified bands and colormap, skipping pixel values of -10000.0 and 65536 from the plot.
    Automatically sets vmin and vmax based on the image data.

    Parameters:
    - file (str): The path to the raster file.
    - bands (tuple): A tuple of band indices to be displayed.
    - cmap (str): The colormap to be used for the plot.
    - title (str): The title of the plot.
    - ax (matplotlib.axes.Axes, optional): An optional axes object to plot on. If not provided, a new figure and axes will be created.
    - brightness_factor (float): Factor to adjust brightness of the image (default is 1, meaning no change).
    """
    # Open the raster file
    with rasterio.open(file) as src:
        # Read specified bands
        if len(bands) == 3:
            image_data = src.read(bands)
        elif len(bands) == 1:
            image_data = src.read(bands)
        else:
            raise ValueError("You must provide 1 or 3 bands to display.")

        # Mask special pixel values
        image_data = np.ma.masked_where((image_data == -10000.0) | (image_data == 65536.0), image_data)



        # Normalize the bands if they are outside the range [0, 1]
        normalized_data = np.stack([normalize(band) for band in image_data]) if np.any((image_data < 0) | (image_data > 1)) else image_data

        # Brighten the normalized data
        brightened_data = np.stack([brighten(band, brightness_factor) for band in normalized_data])

        # Set vmin and vmax based on the non-masked data
        vmin = np.min(brightened_data)
        vmax = np.max(brightened_data)

    # Plot the raster data with calculated vmin and vmax
    show(brightened_data, cmap=cmap, title=title, ax=ax, vmin=vmin, vmax=vmax)

def contour(file):
    """
    Plots contour lines on a raster image.

    Parameters:
    - file (str): The path to the raster file for which the contours will be plotted.

    How it works:
    1. **Open the raster file**:
        - The function uses `rasterio.open(file)` to open the specified raster file.

    2. **Create a figure and axes**:
        - A new figure and axes are created using `pyplot.subplots`, setting the figure size to 12x12 inches.

    3. **Display the raster image**:
        - The function displays the first band of the raster file using the `show` function with a grayscale colormap (`'Greys_r'`) and no interpolation.

    4. **Plot contour lines**:
        - Contour lines are added to the plot by calling `show` again with the same raster data, enabling contour plotting.

    5. **Show the plot**:
        - The plot is displayed using `pyplot.show()`.

    Example usage:
    contour('T60GVV.tif')
    """
    src = rasterio.open(file)
    fig, ax = pyplot.subplots(1, figsize=(12, 12))
    show((src, 1), cmap='Greys_r', interpolation='none', ax=ax)
    show((src, 1), contour=True, ax=ax)
    pyplot.show()


def hist(file, bin=50, title="Histogram"):
    """
    Plots a histogram for the pixel values in a raster file.

    Parameters:
    - file (str): The path to the raster file for which the histogram will be generated.
    - bin (int, optional): The number of bins to divide the pixel values into. Default is 50.
    - title (str, optional): The title of the histogram plot. Default is "Histogram".

    How it works:
    1. **Open the raster file**:
        - The function uses `rasterio.open(file)` to open the specified raster file.

    2. **Generate a histogram**:
        - The `show_hist` function from the `rasterio.plot` module is used to generate the histogram of pixel values. The number of bins is determined by the `bin` parameter.
        - The histogram is displayed as a filled step plot with the following settings:
            - `lw=0.0`: Line width is set to 0, meaning the histogram is filled rather than outlined.
            - `stacked=False`: The histogram is not stacked.
            - `alpha=0.3`: The transparency level of the histogram fill.
            - `histtype='stepfilled'`: The histogram is plotted as filled steps.

    3. **Display the histogram**:
        - The histogram is displayed with the specified title.

    Example usage:
    hist('T60GVV.tif', bin=100, title="Raster Pixel Value Distribution")
    """
    src = rasterio.open(file)
    show_hist(
        src, bins=bin, lw=0.0, stacked=False, alpha=0.3,
        histtype='stepfilled', title=title)

import math
def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great-circle distance between two points on the Earth
    specified by their longitude and latitude.

    Parameters:
    - lon1: Longitude of the first point in decimal degrees
    - lat1: Latitude of the first point in decimal degrees
    - lon2: Longitude of the second point in decimal degrees
    - lat2: Latitude of the second point in decimal degrees

    Returns:
    - Distance between the two points in kilometers
    """
    
    # Convert latitude and longitude from degrees to radians
    lon1_rad = math.radians(lon1)
    lat1_rad = math.radians(lat1)
    lon2_rad = math.radians(lon2)
    lat2_rad = math.radians(lat2)
    
    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(dlon / 2) ** 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Radius of the Earth in kilometers (mean radius)
    radius = 6371.0
    
    # Calculate the distance
    distance = radius * c
    
    return distance


import os
from glob import glob
import rasterio

def stack(input_folder, output_file):
    """
    Stacks multiple raster files in a folder (excluding subfolders) into a single raster file,
    combining their data into separate bands. The band names are derived from the last three 
    characters before '.tif' in each file name.

    Parameters:
    - input_folder (str): The folder path containing the raster files to be stacked.
    - output_file (str): The file path for the output stacked raster.

    Returns:
    - str: The file path of the created stacked raster file.
    """
    # Get all .tif files in the input folder (excluding subfolders)
    input_files = glob(os.path.join(input_folder, "*.tif"))
    
    if not input_files:
        raise ValueError("No TIFF files found in the input folder.")

    # Generate band names from the last three characters before '.tif' in file names
    band_names = [os.path.splitext(os.path.basename(f))[-2][-3:].lower() for f in input_files]

    # Read metadata of the first file
    with rasterio.open(input_files[0]) as src0:
        meta = src0.meta

    # Update meta to reflect the number of layers
    meta.update(count=len(input_files))

    # Create the output stacked raster file
    with rasterio.open(output_file, 'w', **meta) as dst:
        for idx, layer in enumerate(input_files):
            with rasterio.open(layer) as src:
                dst.write_band(idx + 1, src.read(1))
                dst.set_band_description(idx + 1, band_names[idx])

    return output_file


def bandnames(input_raster, band_names):
    """
    Updates the band descriptions of an existing raster file.

    Parameters:
    - input_raster (str): The file path of the raster file whose band names will be updated.
    - band_names (list): A list of new names for the bands in the raster file. 
                         The length of this list must match the number of bands in the raster.

    How it works:
    1. **Open Raster File**: The function opens the specified raster file in read/write mode ('r+').
    
    2. **Update Band Names**: It assigns the provided `band_names` as descriptions for the bands in the raster file. 
       The descriptions are stored as a tuple.

    3. **Ensure Matching Length**: It is the user's responsibility to ensure that the length of `band_names` 
       matches the number of bands in the raster file; otherwise, an error may occur.

    Example usage:
    bandnames('example_raster.tif', ['Band 1', 'Band 2', 'Band 3'])
    """
    with rasterio.open(input_raster, 'r+') as src:
        src.descriptions = tuple(band_names)



def getFeatures(geo):
    """
    Parses features from a GeoDataFrame to a format compatible with rasterio.

    Parameters:
    - geo (GeoDataFrame): A GeoDataFrame containing geospatial features.

    Returns:
    - List[dict]: A list containing geometries extracted from the GeoDataFrame.
    
    How it works:
    1. **Convert to JSON**: The function converts the GeoDataFrame to a JSON format using the `to_json` method.
    
    2. **Extract Geometry**: It then parses the JSON to retrieve the geometry of the first feature. 
       This is done by accessing the 'features' key in the JSON dictionary and extracting the geometry 
       of the first feature in the list.

    Note:
    - The function currently returns only the geometry of the first feature. If the GeoDataFrame contains 
      multiple features and you want all of them, you may need to modify the function to iterate over all features.

    Example usage:
    features = getFeatures(my_geodataframe)
    """
    import json
    return [json.loads(geo.to_json())['features'][0]['geometry']]

    
def clip(raster_file, shapefile, output_file, epsg_code=None):
    """
    Clips a raster file using a shapefile and saves the output to a specified file.

    Parameters:
    - raster_file (str): Path to the input raster file.
    - shapefile (str): Path to the shapefile used for clipping.
    - output_file (str): Path to the output file where the clipped raster will be saved.
    - epsg_code (int, optional): EPSG code for the coordinate reference system of the output.
      If None, the EPSG code of the input file will be used.

    Returns:
    - None: The function saves the clipped raster to the specified output file.
    """
    # Read the shapefile to get geometries for clipping
    geo = gpd.read_file(shapefile)
    coords = geo.geometry.values  # Get the geometries

    # Open the input raster
    with rasterio.open(raster_file) as src:
        # Clip the raster with the shapefile's geometry
        out_img, out_transform = mask(dataset=src, shapes=coords, crop=True)

        # Copy the metadata
        out_meta = src.meta.copy()
        band_names = src.descriptions

        # Use the input raster's EPSG code if epsg_code is None
        if epsg_code is None:
            epsg_code = src.crs.to_epsg()

        # Update metadata
        out_meta.update({
            "driver": "GTiff",
            "height": out_img.shape[1],
            "width": out_img.shape[2],
            "transform": out_transform,
            "crs": f"EPSG:{epsg_code}",
        })

    # Save the clipped raster to the specified output file
    with rasterio.open(output_file, "w", **out_meta) as dest:
        dest.write(out_img)

    # Set band names if provided
    if band_names:
        bandnames(output_file, band_names)


def extract(rf, shp, all_touched=False):
    """
    Extracts raster values at the locations of features in a shapefile.

    Parameters:
    - rf (str): Path to the input raster file.
    - shp (str): Path to the shapefile containing geometries for extraction.
    - all_touched (bool, optional): If True, all pixels touched by the geometry will be included. 
                                     If False, only the pixels that are completely within the geometry are extracted. Default is False.

    Returns:
    - gdf_extracted (GeoDataFrame): A GeoDataFrame containing the extracted raster values and their corresponding geometries.

    How it works:
    1. **Read Shapefile**: The function reads the specified shapefile using GeoPandas to obtain geometries for extraction.
    
    2. **Open Raster**: The raster file is opened using Rasterio to access its pixel values.
    
    3. **Initialize Lists**: Empty lists are initialized to store pixel coordinates and the extracted data.

    4. **Iterate Through Features**: The function iterates through each feature in the GeoDataFrame:
        - **Mask Creation**: A mask is created based on the feature geometry to determine which pixels are within or touched by the geometry.
        - **Data Extraction**: For each band in the raster, the pixel values are extracted using the mask and stored in a dictionary.
        - **Coordinate Calculation**: The row and column indices of the masked pixels are obtained, and their geographical coordinates are calculated.
        - **DataFrame Creation**: A DataFrame is created for the extracted raster values, and attributes from the shapefile are included.

    5. **Combine DataFrames**: All extracted DataFrames are concatenated into a single GeoDataFrame.

    Example usage:
    extracted_data = extract('input_raster.tif', 'features.shp', all_touched=True)
    """
    gdf = gpd.read_file(shp)
    src = rasterio.open(rf)
    pixel_coords = []
    extracted_data = []

    for idx, row in gdf.iterrows():
        geom = row.geometry
        attributes = row.to_dict()  # Get all columns as a dictionary

        mask = rasterio.features.geometry_mask([geom], src.shape, transform=src.transform, invert=True, all_touched=all_touched)
        data = {}
        for i in range(src.count):
            band = src.read(i + 1, masked=True)[mask]
            column_name = f'band_{i+1}'
            data[column_name] = band.flatten()

        row, col = np.where(mask == True)
        coords = [Point(src.xy(r, c)) for r, c in zip(row, col)]

        # Create a DataFrame for the extracted data
        extracted_df = pd.DataFrame(data)
        
        # Include all shapefile columns as attributes
        for key, value in attributes.items():
            extracted_df[key] = value
        
        extracted_df['geometry'] = coords
        
        extracted_data.append(extracted_df)

    gdf_extracted = pd.concat(extracted_data, ignore_index=True)
    gdf_extracted = gpd.GeoDataFrame(gdf_extracted, geometry='geometry', crs=src.crs)

    return gdf_extracted


def savetif(output, gdf, colname='FVC', input_raster=None, resolution=10, dtype=rasterio.float32):
    """
    Saves a GeoDataFrame as a raster file (GeoTIFF) by rasterizing its geometries.

    Parameters:
    - output (str): Path to the output raster file.
    - gdf (GeoDataFrame): A GeoDataFrame containing the geometries to be rasterized.
    - colname (str, optional): The name of the column in the GeoDataFrame whose values will be used to populate the raster. Default is 'FVC'.
    - input_raster (str, optional): Path to an input raster file to obtain resolution from. If not provided, the specified resolution will be used.
    - resolution (int, optional): Desired resolution for the output raster in the same units as the geometries. Default is 10.
    - dtype: Data type of the raster values. Default is `rasterio.float32`.

    Returns:
    - None: The function writes a raster file at the specified output path.

    How it works:
    1. **Bounding Box Calculation**: The function calculates the bounding box of the provided GeoDataFrame to determine the extent of the raster.
    
    2. **Resolution Determination**: If an input raster is provided, the function retrieves its resolution; otherwise, it uses the specified default resolution.

    3. **Output Raster Metadata**: The function prepares metadata for the output raster, including its dimensions, data type, coordinate reference system (CRS), and transform based on the bounding box.

    4. **Rasterization**: The geometries in the GeoDataFrame are rasterized using the specified column's values:
        - A generator of geometry-value pairs is created.
        - The `rasterio.features.rasterize` function is called to create a raster array from these geometries.
        - The background value is set to 255, and the rasterization method is specified.

    5. **Writing the Raster**: The resulting raster array is written to the output file.

    Example usage:
    savetif('output_raster.tif', gdf, colname='Vegetation_Index', input_raster='input.tif', resolution=10)
    """
    bbox = gdf.total_bounds
    xmin, ymin, xmax, ymax = bbox

    if input_raster:        
        with rasterio.open(input_raster) as src:            
            res = src.res[0]
    else:
        res = resolution  # Default desired resolution

    w = int(xmax - xmin) // res
    h = int(ymax - ymin) // res
    out_meta = {
        "driver": "GTiff",
        "dtype": dtype,
        "height": h,
        "width": w,
        "count": 1,
        "crs": gdf.crs,
        "transform": transform.from_bounds(xmin, ymin, xmax, ymax, w, h),
        "compress": 'lzw'
    }
    with rasterio.open(output, 'w+', **out_meta) as out:
        out_arr = out.read(1)

        # This is where we create a generator of geom, value pairs to use in rasterizing
        shapes = ((geom, value)
                  for geom, value in zip(gdf.geometry, gdf[colname]))
        burned = features.rasterize(shapes, out=out_arr,
                                    out_shape=out.shape,
                                    transform=out.transform,
                                    all_touched=True,
                                    fill=255,   # Background value
                                    merge_alg=MergeAlg.replace,
                                    dtype=dtype)

        out.write_band(1, burned)

def mergecsv(path, outfile='combined_all.csv'):
    """
    Merges all CSV files in a directory into a single CSV file.

    Parameters:
    - path (str): The directory where CSV files are located.
    - outfile (str, optional): The name of the output merged CSV file. Default is 'combined_all.csv'.

    How it works:
    1. **Get a list of CSV files**: 
        - The `glob` function is used to search the directory (specified by `path`) for all `.csv` files and returns their file paths.
    
    2. **Initialize an empty DataFrame**: 
        - An empty DataFrame `df` is created to store the merged data from all CSV files.
    
    3. **Loop through each CSV file and merge them**:
        - The function iterates over each CSV file in the list of files.
        - Each file is read into a temporary DataFrame (`df0`) using `pd.read_csv`.
        - The contents of `df0` are concatenated with the existing data in `df` using `pd.concat`. This accumulates data from all CSV files.
    
    4. **Reset the index of the merged DataFrame**: 
        - The index of the merged DataFrame is reset using `df.reset_index(drop=True)` to ensure that it is sequential and doesn't retain any index from the original CSV files.
    
    5. **Print the shape of the merged DataFrame**:
        - It prints the shape (rows, columns) of the final merged DataFrame, giving the user a quick summary of how many rows and columns it contains.
    
    6. **Save the merged DataFrame to a CSV file**:
        - The merged DataFrame is saved to the output file (`outfile`) using `df.to_csv`. The default name is 'combined_all.csv', but you can specify a different name.

    Example usage:
    merged_df = mergecsv('/path/to/csv_files')
    """
    # Get a list of CSV files using glob
    files = glob(path + "/*.csv")

    # Check if any CSV files are found
    if not files:
        print("No CSV files found in the specified directory.")
        return None  # Return None if no files are found

    # Initialize an empty DataFrame to store the merged data
    df = pd.DataFrame()

    # Loop through each CSV file and merge them into df
    for f in files:
        try:
            df0 = pd.read_csv(f)
            df = pd.concat([df, df0], ignore_index=True)
        except Exception as e:
            print(f"Error reading {f}: {e}")

    # Reset the index of the merged DataFrame
    df.reset_index(drop=True, inplace=True)

    # Print the shape of the merged DataFrame
    print("Shape of the merged DataFrame:", df.shape)

    # Save the merged DataFrame to a CSV file    
    df.to_csv(outfile, index=False)

    return df  # Return the merged DataFrame

import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

def reproject(input_raster, output_raster, target_crs):
    """
    Reprojects a raster to a different coordinate reference system (CRS).
    
    Parameters:
    input_raster (str): Path to the input raster file.
    output_raster (str): Path to the output raster file.
    target_crs (str or dict): The target CRS in a format recognized by rasterio (e.g., 'EPSG:4326').
    
    Returns:
    None
    """
    with rasterio.open(input_raster) as src:
        # Get the transform, width, and height of the reprojected raster
        transform, width, height = calculate_default_transform(
            src.crs, target_crs, src.width, src.height, *src.bounds)
        
        # Update metadata for the new CRS
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': target_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        
        # Reproject and write to the new file
        with rasterio.open(output_raster, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.nearest
                )

def ndvi(raster_file, output_file, red_band=3, nir_band=4):
    """
    Calculates the Normalized Difference Vegetation Index (NDVI) from red and near-infrared (NIR) bands
    and saves the output as a raster file.

    Parameters:
    raster_file (str): Path to the input raster file containing the bands.
    output_file (str): Path to the output raster file where the NDVI values will be saved.
    red_band (int, optional): The band index for the red band (1-based index). Default is 3.
    nir_band (int, optional): The band index for the near-infrared (NIR) band (1-based index). Default is 4.

    Returns:
    str: The path to the output NDVI raster file.
    """
    # Open the raster file
    with rasterio.open(raster_file) as src:
        # Read the specified bands (note that rasterio uses 1-based indexing)
        red = src.read(red_band)
        nir = src.read(nir_band)

        # Prepare metadata for the output NDVI raster
        meta = src.meta.copy()
        meta.update({
            'count': 1,                  # Only one band for NDVI
            'dtype': 'float32',          # Set the data type for NDVI
            'compress': 'lzw',           # Optional: compression method
        })

    # Avoid division by zero
    np.seterr(divide='ignore', invalid='ignore')

    # Calculate NDVI
    ndvi = (nir - red) / (nir + red)

    # Handle NaN values by setting them to -10
    ndvi = np.nan_to_num(ndvi, nan=-10.0)

    # Set NDVI values > 1 or < -1 to -10
    ndvi[(ndvi > 1) | (ndvi < -1)] = -10

    # Save the NDVI as a raster file
    with rasterio.open(output_file, 'w', **meta) as dst:
        dst.write(ndvi, 1)  # Write NDVI to the first band

    return output_file





def zonalstats(raster_file, vector_file, stats=['mean', 'max', 'min', 'std']):
    """
    Calculates zonal statistics for each polygon in a vector file based on the values of a raster file.
    
    Parameters:
    raster_file (str): Path to the input raster file.
    vector_file (str): Path to the input vector file (shapefile or GeoJSON).
    stats (list): A list of statistics to calculate (default is ['mean', 'max', 'min', 'std']).
                  Other options include 'sum', 'median', 'count', 'range', 'nodata', 'percentile_X' (where X is a number), etc.
    
    Returns:
    GeoDataFrame: A GeoDataFrame containing the original vector file and the calculated statistics.
    """
    # Load the vector file
    vector_data = gpd.read_file(vector_file)
    
    # Calculate zonal statistics
    zone_stats = zonal_stats(vector_file, raster_file, stats=stats, geojson_out=True)
    
    # Convert the zonal stats into a GeoDataFrame
    stats_gdf = gpd.GeoDataFrame.from_features(zone_stats)
    
    # Merge the statistics with the original vector data
    result = vector_data.merge(stats_gdf, on='geometry', how='left')
    
    return result
import rasterio
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import shape
import numpy as np

def convras(raster_file, output_shapefile, field_name='value'):
    """
    Converts a raster file to a vector format (polygons) and saves it as a shapefile.
    
    Parameters:
    raster_file (str): Path to the input raster file.
    output_shapefile (str): Path to save the output vector (shapefile).
    field_name (str): The name of the attribute field in the output shapefile to store raster values (default is 'value').
    
    Returns:
    None
    """
    # Open the raster file
    with rasterio.open(raster_file) as src:
        # Read the raster data
        image = src.read(1)  # Assuming single-band raster
        transform = src.transform
        
        # Mask out nodata values if any
        mask = image != src.nodata

        # Generate shapes (polygons) from the raster data
        results = (
            {'properties': {field_name: v}, 'geometry': s}
            for s, v in shapes(image, mask=mask, transform=transform)
        )

        # Convert results to a list of geometries
        geoms = list(results)

    # Convert geometries to a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(geoms, crs=src.crs)
    
    # Save the vector data to a shapefile
    gdf.to_file(output_shapefile, driver='ESRI Shapefile')
import rasterio
from rasterio.enums import Resampling

def resample(input_raster, output_raster, scale_factor=2, resampling_method='bilinear'):
    """
    Resamples a raster to a different resolution using a given scale factor.
    
    Parameters:
    input_raster (str): Path to the input raster file.
    output_raster (str): Path to save the resampled raster file.
    scale_factor (float): The scale factor by which to adjust the resolution (default is 2).
                          Values greater than 1 increase resolution (downsampling), and
                          values less than 1 decrease resolution (upsampling).
    resampling_method (str): The resampling method to use (default is 'bilinear'). Other options include
                             'nearest', 'cubic', 'lanczos', etc.
    
    Returns:
    None
    """
    # Map resampling method to rasterio's Resampling enum
    resampling_methods = {
        'nearest': Resampling.nearest,
        'bilinear': Resampling.bilinear,
        'cubic': Resampling.cubic,
        'lanczos': Resampling.lanczos
    }

    if resampling_method not in resampling_methods:
        raise ValueError(f"Invalid resampling method. Choose from {list(resampling_methods.keys())}")

    with rasterio.open(input_raster) as src:
        # Calculate the new dimensions based on the scale factor
        new_width = int(src.width * scale_factor)
        new_height = int(src.height * scale_factor)
        
        # Calculate the transform for the new raster
        new_transform = src.transform * src.transform.scale(
            (src.width / new_width),
            (src.height / new_height)
        )

        # Update metadata with new width, height, and transform
        kwargs = src.meta.copy()
        kwargs.update({
            'width': new_width,
            'height': new_height,
            'transform': new_transform
        })

        # Resample and save the output raster
        with rasterio.open(output_raster, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                # Read the data from the source
                data = src.read(i, out_shape=(new_height, new_width), resampling=resampling_methods[resampling_method])
                
                # Write the resampled data to the destination
                dst.write(data, i)
import rasterio
import numpy as np

def stats(raster_file):
    """
    Calculates basic statistics (min, max, mean, std) for a raster file.
    
    Parameters:
    raster_file (str): Path to the input raster file.
    
    Returns:
    dict: A dictionary containing the min, max, mean, and standard deviation of the raster.
    """
    with rasterio.open(raster_file) as src:
        # Read the raster data (assuming single-band raster)
        data = src.read(1)
        
        # Mask out nodata values (if any)
        data = np.ma.masked_equal(data, src.nodata)
        
        # Calculate statistics
        stats = {
            'min': np.min(data),
            'max': np.max(data),
            'mean': np.mean(data),
            'std': np.std(data)
        }
        
        return stats
