from datetime import datetime
from dataclasses import dataclass, field
from typing import List
from UV_arxiv.uv_arxiv_index import uv_files
from common.coordinates import get_ilon, get_ilat
import netCDF4 as nc
import numpy as np
import pandas as pd

@dataclass
class RequestPrecise:
    filename: str
    start_index: int
    end_index: int
    latitude_index: int
    longitude_index: int

    def get_uv_dose(self, uv_type : str):
        src = nc.Dataset(self.filename, 'r')
        uvd_src = src.groups['PRODUCT'].variables[uv_type]

        return np.sum(uvd_src[self.start_index:self.end_index, self.latitude_index, self.longitude_index])

    def get_uv_max(self, uv_type: str):
        src = nc.Dataset(self.filename, 'r')
        uvd_src = src.groups['PRODUCT'].variables[uv_type]

        return np.max(uvd_src[self.start_index:self.end_index, self.latitude_index, self.longitude_index])

    def get_uv_min(self, uv_type : str):
        src = nc.Dataset(self.filename, 'r')
        uvd_src = src.groups['PRODUCT'].variables[uv_type]

        return np.min(uvd_src[self.start_index:self.end_index, self.latitude_index, self.longitude_index])


    def get_uv_dose_clear(self):
        return self.get_uv_dose('uvd_clear')

    def get_uv_dose_cloudy(self):
        return self.get_uv_dose('uvd_cloudy')


@dataclass
class RequestEstimate:
    latitude_index: int
    longitude_index: int
    days_per_months: np.ndarray = field(default_factory=lambda: np.zeros(12))

    def __post_init__(self):
        if not isinstance(self.days_per_months, np.ndarray):
            raise TypeError("array must be a numpy ndarray")
        if self.days_per_months.size != 12:
            raise ValueError("array must have exactly 12 elements")

    source_path = "estimator/uv_max.nc"

    def get_uv_dose(self, uv_type : str):
        src = nc.Dataset(self.source_path, 'r')
        uvd_values = src.groups['PRODUCT'].variables[uv_type][:, self.latitude_index, self.longitude_index]

        return float(np.dot(self.days_per_months, uvd_values))

    def get_uv_dose_clear(self):
        return self.get_uv_dose('uvd_clear')


    def get_uv_dose_cloudy(self):
        return self.get_uv_dose('uvd_cloudy')

@dataclass
class Rig:
    start_date: datetime
    end_date: datetime
    latitude: float
    longitude: float

    def __repr__(self):
        return f"Rig(start={self.start_date}, end={self.end_date}, longitude={self.longitude}, latitude={self.latitude})"

    def to_precise_request(self) -> [RequestPrecise]:
        year_start = self.start_date.year
        year_end = self.end_date.year
        if year_start != year_end:
            rig_1 = Rig(self.start_date, datetime(year_start, 12, 31, 23, 59, 59), self.longitude, self.latitude)
            rig_2 = Rig(datetime(year_start + 1, 1, 1, 0, 0, 0), self.end_date, self.longitude, self.latitude)
            return rig_1.to_precise_request() + rig_2.to_precise_request()
        else:
            filename = uv_files[year_start]
            start_index = (self.start_date - datetime(year_start, 1, 1)).days
            end_index = (self.end_date - datetime(year_start, 1, 1)).days + 1
            lat_index = get_ilat(self.latitude)
            lon_index = get_ilon(self.longitude)
            return [RequestPrecise(filename, start_index, end_index, lat_index, lon_index)]

    def to_estimate_request(self) -> RequestEstimate:
        all_dates = pd.date_range(self.start_date, self.end_date)
        days_per_month = np.zeros(12, dtype=int)

        for month in range(1, 13):
            days_per_month[month - 1] = all_dates[all_dates.month == month].size

        return RequestEstimate(get_ilat(self.latitude), get_ilon(self.longitude), days_per_month)


@dataclass
class Record:
    rigs: List[Rig] = field(default_factory=list)

    def to_precise_request(self) -> [RequestPrecise]:
        requests = []
        for rig in self.rigs:
            requests.extend(rig.to_precise_request())
        return requests

    def to_estimate_request(self) -> [RequestEstimate]:
        return [rig.to_estimate_request() for rig in self.rigs]

    def __repr__(self):
        return f"Record(rigs={self.rigs})"
