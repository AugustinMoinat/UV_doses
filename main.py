'''
 Extract the TEMIS UV index or UV dose data for a given location.

 From a 'europe' file extraction takes a few seconds,
 from a 'world' file extraction may take some 30 seconds.

 usage:  uvnctimeseries.py -h

 source: https://www.temis.nl/uvradiation/

'''

import numpy as np
import netCDF4 as nc
import sys
import os
from UV_arxiv.uv_arxiv_index import uv_files

import warnings

warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


# ==================================================================
# Main part
# ==================================================================

if __name__ == "__main__":

    # Configuration
    # -------------

    # import argparse
    #
    # dataUrl = "https://www.temis.nl/uvradiation/UVarchive/uvncfiles.php"
    #
    # parser = argparse.ArgumentParser(description= \
    #                                      'Extract the TEMIS UV index or UV dose data for a given location ' + \
    #                                      'from a either a file with one year or data or a climatology file, ' + \
    #                                      'which can be downloaded from %s || The output is written to the screen.' % (
    #                                          dataUrl))
    #
    # lonStr = 'longitude, decimal degrees in range [-180:+180]  '
    # parser.add_argument('lon', metavar='LON', help=lonStr)
    #
    # latStr = 'latitude, decimal degrees in range [-90:+90]'
    # parser.add_argument('lat', metavar='LAT', help=latStr)
    #
    # fileStr = 'netCDF file with the UV index or UV dose data'
    # parser.add_argument('file', metavar='FILE', help=fileStr)
    #
    # args = parser.parse_args()

    # Check arguments
    # ---------------

    # Check whether the given data file exists

    ncFile = uv_files[2023]
    out_file = 'uv_max.nc'

    if not os.path.isfile(ncFile):
        print(' *** Error: given netCDF file does not exist')
        sys.exit(1)

    src = nc.Dataset(ncFile, 'r')

    print(src.groups['PRODUCT'])
    print(src.groups['PRODUCT'].dimensions)
    print(src.groups['PRODUCT'].variables)

    lat = 45
    lon = 0
    ilat = getIlat(lat)
    ilon = getIlon(lon)

    # Create the new NetCDF file
    dst = nc.Dataset(out_file, 'w')

    # 1. Copy latitude and longitude dimensions
    dst.createDimension('latitude', len(src.groups['PRODUCT'].dimensions['latitude']))
    dst.createDimension('longitude', len(src.groups['PRODUCT'].dimensions['longitude']))
    dst.createDimension('month', 12)  # Create new dimension for months (12 months in a year)

    # 2. Copy latitude, longitude, and index variables
    # Copy latitude
    lat_src = src.groups['PRODUCT'].variables['latitude']
    lat_dst = dst.createVariable('latitude', lat_src.datatype, ('latitude',))
    lat_dst[:] = lat_src[:]

    # Copy longitude
    lon_src = src.groups['PRODUCT'].variables['longitude']
    lon_dst = dst.createVariable('longitude', lon_src.datatype, ('longitude',))
    lon_dst[:] = lon_src[:]

    # Copy latitude_index and longitude_index
    lat_idx_src = src.groups['PRODUCT'].variables['latitude_index']
    lat_idx_dst = dst.createVariable('latitude_index', lat_idx_src.datatype, ('latitude',))
    lat_idx_dst[:] = lat_idx_src[:]

    lon_idx_src = src.groups['PRODUCT'].variables['longitude_index']
    lon_idx_dst = dst.createVariable('longitude_index', lon_idx_src.datatype, ('longitude',))
    lon_idx_dst[:] = lon_idx_src[:]

    # 3. Create a variable for month names
    month_names = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], dtype='S3')
    months_var = dst.createVariable('month_names', 'S1', ('month',))
    months_var[:] = month_names[:]  # Convert to char array (S1 format)

    # 4. Coalesce daily data into monthly data (assuming the original data is for 365 days)
    def monthly_maximum(daily_data):
        # Create an empty array to store the monthly aggregated data
        monthly_data = np.zeros((12, daily_data.shape[1], daily_data.shape[2]))

        # Indices for days corresponding to each month

        months_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        months_index_start = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        months_index_end = [30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i, n in enumerate(months_lengths):
            if i < 11:
                months_index_start[i + 1] = months_index_start[i] + n
                months_index_end[i + 1] = months_index_end[i] + n
        month_day_indices = zip(months_index_start, months_index_end)

        # Aggregate by month (e.g., by averaging)
        for month, (start, end) in enumerate(month_day_indices):
            monthly_data[month, :, :] = np.max(daily_data[start:end+1, :, :], axis=0)

        return monthly_data


    # Copy and coalesce the uvd_clear and uvd_cloudy data
    uvd_clear_src = src.groups['PRODUCT'].variables['uvd_clear']
    uvd_clear_dst = dst.createVariable('uvd_clear', 'f4', ('month', 'latitude', 'longitude'))
    uvd_clear_dst[:] = monthly_maximum(uvd_clear_src[:])

    uvd_cloudy_src = src.groups['PRODUCT'].variables['uvd_cloudy']
    uvd_cloudy_dst = dst.createVariable('uvd_cloudy', 'f4', ('month', 'latitude', 'longitude'))
    uvd_cloudy_dst[:] = monthly_maximum(uvd_cloudy_src[:])

    # Close both files
    src.close()
    dst.close()

    # --------

    sys.exit(0)
