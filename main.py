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
from estimator.compute_uv_max.create_month_nc import create_month_nc
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
    out_file = 'estimator/uv_max.nc'

    if not os.path.isfile(ncFile):
        print(' *** Error: given netCDF file does not exist')
        sys.exit(1)

    create_month_nc(out_file, ncFile)

    src = nc.Dataset(ncFile, 'r')

    # Create the new NetCDF file
    dst = nc.Dataset(out_file, 'r+')
    print(dst.dimensions)

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
