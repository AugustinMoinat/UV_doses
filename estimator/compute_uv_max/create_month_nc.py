import netCDF4 as nc
import numpy as np
import sys
import os


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