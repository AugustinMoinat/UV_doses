from datetime import datetime
from dataclasses import dataclass
from UV_arxiv.uv_arxiv_index import uv_files
from common.coordinates import get_ilon, get_ilat
import netCDF4 as nc
import numpy as np

@dataclass
class RequestNC:
    filename: str
    start_index: int
    end_index: int
    latitude_index: int
    longitude_index: int

    def get_uv_dose(self):
        src = nc.Dataset(self.filename, 'r')
        uvd_clear_src = src.groups['PRODUCT'].variables['uvd_clear']

        return np.sum(uvd_clear_src[self.start_index:self.end_index, self.latitude_index, self.longitude_index])

class Rig:
    def __init__(self, start_date: datetime, end_date: datetime, latitude: float, longitude: float):
        self.start_date = start_date
        self.end_date = end_date
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Rig(start={self.start_date}, end={self.end_date}, longitude={self.longitude}, latitude={self.latitude})"

    def to_request(self) -> [RequestNC]:
        year_start = self.start_date.year
        year_end = self.end_date.year
        if year_start != year_end:
            rig_1 = Rig(self.start_date, datetime(year_start, 12, 31, 23, 59, 59), self.longitude, self.latitude)
            rig_2 = Rig(datetime(year_start + 1, 1, 1, 0, 0, 0), self.end_date, self.longitude, self.latitude)
            return rig_1.to_request() + rig_2.to_request()
        else:
            filename = uv_files[year_start]
            start_index = (self.start_date - datetime(year_start, 1, 1)).days
            end_index = (self.end_date - datetime(year_start, 1, 1)).days + 1
            lat_index = get_ilat(self.latitude)
            lon_index = get_ilon(self.longitude)
            return [RequestNC(filename, start_index, end_index, lat_index, lon_index)]


class Record:
    def __init__(self, rigs: [Rig]):
        self.rigs = rigs

    def to_request(self):
        requests = []
        for rig in self.rigs:
            requests.extend(rig.to_request())
        return requests

    def __repr__(self):
        return f"Record(rigs={self.rigs})"
