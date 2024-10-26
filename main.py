'''
 Extract the TEMIS UV index or UV dose data for a given location.

 From a 'europe' file extraction takes a few seconds,
 from a 'world' file extraction may take some 30 seconds.

 usage:  uvnctimeseries.py -h

 source: https://www.temis.nl/uvradiation/

'''

from estimator.compute_uv_max.create_month_file import compute_month_max



# ==================================================================
# Main part
# ==================================================================

if __name__ == "__main__":
    compute_month_max()