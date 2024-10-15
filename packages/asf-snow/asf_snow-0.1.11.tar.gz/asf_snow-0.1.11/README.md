# asf-snow
Evaluation of Snow depths for the CRREL Arctic Trafficability with the spicy-snow python module (https://github.com/SnowEx/spicy-snow). The spicy-snow uses volumetric scattering at C-band to calculate snow depths from Sentinel-1 imagery using Lieven et al.'s 2021 technique.



List of Programs

sentinel1_snow.py, produces Sentinel1-derived snow depth product according to the spatial area and time range

compare_sentinel1_snow_depth_to_snex.py, calculate the statistic of sentinel1 and SNEX snow depth data

analyze_snex.py, includes codes to read different kinds of SNEX csv files

analyze_sentinel1_snow.py, include all kinds of draw plot functions

combine_multiple_statistic_results.py, combine multiple monthly statistic files, and draw the histogram plot



compare_sentinel1_snow_depth_to_snex_lidar.py, calculate the statistic of sentinel1 and Lidar snow depth data, and draw the scatter plot


compare_sentinel1_snow_depth_to_snotel.py, calculate statistic of Sentinel1 and SNOTEL snow depth time series

draw_s1_snotel_plot.py, draw Sentinel1-derived snow depth and SNOTEL snow depth curves, the difference curve, and histograms of s1 and SNOTEL snow depth




