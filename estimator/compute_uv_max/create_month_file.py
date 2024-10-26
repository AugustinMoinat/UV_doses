import netCDF4 as nc
import numpy as np
import sys
import os
from UV_arxiv.uv_arxiv_index import uv_files


def compute_month_max():
    files_index = list(uv_files.keys())
    ncFile = uv_files[files_index[0]]
    out_file = 'estimator/uv_max.nc'

    create_month_nc(out_file, ncFile)

    # Create the new NetCDF file
    dst = nc.Dataset(out_file, 'r+')
    print(dst.dimensions)

    uvd_clear = []
    uvd_cloudy = []

    for key in files_index:
        src = nc.Dataset(uv_files[key], 'r')

        uvd_clear_src = src.groups['PRODUCT'].variables['uvd_clear']
        uvd_clear.append(monthly_maximum(uvd_clear_src[:]))

        uvd_cloudy_src = src.groups['PRODUCT'].variables['uvd_cloudy']
        uvd_cloudy.append(monthly_maximum(uvd_cloudy_src[:]))

        src.close()
    uvd_clear_dst = dst.createVariable('uvd_clear', 'f4', ('month', 'latitude', 'longitude'))
    uvd_clear_dst[:] = np.maximum.reduce(uvd_clear)

    uvd_cloudy_dst = dst.createVariable('uvd_cloudy', 'f4', ('month', 'latitude', 'longitude'))
    uvd_cloudy_dst[:] = np.maximum.reduce(uvd_cloudy)

    dst.close()

    sys.exit(0)

def create_month_nc(dest_file ,example_file):

    if not os.path.isfile(example_file):
        print(' *** Error: given netCDF file does not exist')
        sys.exit(1)

    src = nc.Dataset(example_file, 'r')

    # Create the new NetCDF file
    dst = nc.Dataset(dest_file, 'w')

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

    # Close both files
    src.close()
    dst.close()


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
        monthly_data[month, :, :] = np.max(daily_data[start:end + 1, :, :], axis=0)

    return monthly_data