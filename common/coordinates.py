
def check_coordinates(lon, lat, nc_file):
    '''
     Make sure that the given coordinate is available within the file,
     which either covers 'world' or 'europe'.

     It returns the grid cell indices to use in the data extraction,
     taking the data coverage into account.
    '''

    with nc.Dataset(nc_file, 'r') as src:

        # The data coverage is specified by global attributes:

        lon_min = src.geospatial_lon_min
        lon_max = src.geospatial_lon_max
        lat_min = src.geospatial_lat_min
        lat_max = src.geospatial_lat_max

        if lon > lon_max or lon < lon_min:
            print(' *** Error: longitude should be in the range [%s:%s]' % (lon_min, lon_max))
            sys.exit(1)

        if lat > lat_max or lat < lat_min:
            print(' *** Error: latitude should be in the range [%s:%s]' % (lat_min, lat_max))
            sys.exit(1)

        # Find the offset index of both coordinates;
        # for data that covers the 'world' both are zero.

        ilon_offset = src.groups['PRODUCT'].variables['longitude_index'][0]
        ilat_offset = src.groups['PRODUCT'].variables['latitude_index'][0]

    # Grid cell indices including the

    ilon = getIlon(lon) - ilon_offset
    ilat = getIlat(lat) - ilat_offset

    return ilon, ilat


# ==================================================================

# Conversion routines of latitude and longitude coordinates in degrees
# to grid cell indices. The index counting is 0-based, that is:
# * longitudes range from 0 (West) to 1439 (East)
# * latitudes  range from 0 (South) to 719 (North)
# and thus covers the full world.
# The grid cells are dlon by dlat = 0.25 by 0.25 degrees

def get_ilon(lon):
    dlon = 360.0 / 1440.0
    return round((lon + 180.0 - dlon / 2.0) / dlon)


def get_ilat(lat):
    dlat = 180.0 / 720.0
    return round((lat + 90.0 - dlat / 2.0) / dlat)

