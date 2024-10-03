# UV Dose Estimation for Webbings

This is the start of a project. So far, there is only a main.py to gather ideas.

This project aims to estimate the total UV dose that webbings are 
exposed to over time. The data used for these estimations comes from 
the [Temis project](https://www.temis.nl/uvradiation/UVarchive/uvncfiles.php), which provides detailed UV radiation data.

## Goals
1. **Small Dataset for Estimation**: 
   - One part of the project is to create a smaller, 
   more manageable version of the dataset. This version allows us to estimate the UV dose a webbing is exposed to, based on a log of its uses and locations.
   
2. **Full Dataset for Exact UV Doses**: 
   - The second part of the project focuses on providing exact UV dose calculations. However, this requires access to the full dataset, which will not be hosted in this repository.

Feel free to explore and contribute!

## Techniques
From the Temis project, we need the "clear-sky & cloud-modified erythemal UV dose". They are the named uvdec_YYYY.nc files and in netcdf4 format.

#### File Dimensions

The dataset includes the following dimensions:

- **latitude (720)**: Represents latitude values (0.25°).
- **longitude (1440)**: Represents longitude values (0.25°).
- **corner (4)**: Used in defining the geographic bounds, likely representing the four corners of grid cells.
- **year (1)**: The dataset covers a single year.
- **days (365)**: Represents daily data for 365 days of the year.

#### File Variables

-*uvd_clear**: (`float32`, dimensions: `days, latitude, longitude`) Represents the daily clear-sky ultraviolet radiation values. The data is stored for each day, at each grid point defined by latitude and longitude.

   
-*uvd_cloudy**: (`float32`, dimensions: `days, latitude, longitude`) epresents the daily cloudy-sky ultraviolet radiation values. The data is stored for each day, at each grid point defined by latitude and longitude.

The file [uv_max.nc](uv_max.nc) is where we want to compile max uv doses over each month. Keeping in mind that we are looking at a safety application, we want to estimate a worst case scenario.
We are also considering the fact that highliners are most likely to rig with beautiful weather.

#### Python Library

This project is using the [netcdf4](https://unidata.github.io/netcdf4-python/) library.