from datetime import datetime
from common.record import Rig, Record, RequestNC


def test_single_year_record():
    # A rig within the same year
    rig1 = Rig(datetime(2022, 2, 15), datetime(2022, 12, 15), 10.0, 50.0)
    record = Record([rig1])
    request_rig = rig1.to_request()
    request_record = record.to_request()

    # No splitting should happen
    assert len(request_rig) == 1
    assert request_rig[0].filename == "UV_arxiv/uvdec2022_world.nc"
    assert request_rig[0].start_index == 30+15
    assert request_rig[0].end_index == 365 - 16
    assert len(request_record) == 1


def test_multiple_years_record():
    # A rig that spans two years
    rig1 = Rig(datetime(2020, 6, 1), datetime(2020, 12, 15), 10.0, 50.0)
    rig2 = Rig(datetime(2021, 6, 1), datetime(2023, 3, 15), 20.0, 60.0)
    record = Record([rig1,rig2])
    request_rig2 = rig2.to_request()
    request_record = record.to_request()

    assert len(request_rig2) == 3
    assert request_rig2[0].start_index == 151
    assert request_rig2[0].end_index == 365
    assert request_rig2[0].filename == "UV_arxiv/uvdec2021_world.nc"
    assert request_rig2[1].start_index == 0
    assert request_rig2[1].end_index == 365
    assert request_rig2[1].filename == "UV_arxiv/uvdec2022_world.nc"
    assert request_rig2[2].start_index == 0
    assert request_rig2[2].end_index == 31 + 28 + 15
    assert request_rig2[2].filename == "UV_arxiv/uvdec2023_world.nc"



    assert len(request_record) == 4
    assert request_record[1].start_index == 151
    assert request_record[1].end_index == 365
    assert request_record[2].start_index == 0
    assert request_record[2].end_index == 365
    assert request_record[3].start_index == 0
    assert request_record[3].end_index == 31 + 28 + 15

def test_request():
    rig1 = Rig(datetime(2023, 2, 15), datetime(2023, 2, 15), 10.0, 50.0)
    rig2 = Rig(datetime(2023, 2, 16), datetime(2023, 2, 18), 10.0, 50.0)
    rig3 = Rig(datetime(2023, 2, 15), datetime(2023, 2, 18), 10.0, 50.0)
    request_rig1 = rig1.to_request()
    dose1 = request_rig1[0].get_uv_dose()
    request_rig2 = rig2.to_request()
    dose2 = request_rig2[0].get_uv_dose()
    request_rig3 = rig3.to_request()
    dose3 = request_rig3[0].get_uv_dose()


    # No splitting should happen
    assert dose1 + dose2 == dose3