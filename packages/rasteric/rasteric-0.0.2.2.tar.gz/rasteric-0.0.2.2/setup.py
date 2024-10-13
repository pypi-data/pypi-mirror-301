from setuptools import find_packages, setup
setup(
    name='rasteric',
    packages=find_packages(include=['rasteric']),
    version='0.0.2.2',
    description='A Comprehensive Geospatial Library',
    author='Thai Tran',
    license='MIT',    
    install_requires=[
    'rasterio>=1.0',      # For raster data handling
    'matplotlib>=3.0',     # For plotting
    'shapely>=1.7',        # For geometric operations
    'geopandas>=0.9',      # For geospatial data manipulation
    'numpy>=1.18',         # For numerical operations
    'pandas>=1.0',         # For data manipulation and analysis
    'scikit-image>=0.18',  # For image processing if needed
    'scikit-learn>=0.24',  # For machine learning if applicable
    'rasterstats',],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)