from datetime import datetime
from common.record import Rig, Record, RequestPrecise, RequestEstimate


def test_single_year_record():
    # A rig within the same year
    rig1 = Rig(datetime(2022, 2, 15), datetime(2022, 12, 15), 10.0, 50.0)
    record = Record([rig1])
    request_rig = rig1.to_precise_request()
    request_record = record.to_precise_request()

    # No splitting should happen
    assert len(request_rig) == 1
    assert request_rig[0].filename == "UV_arxiv/uvdec2022_world.nc"
    assert request_rig[0].start_index == 30+15
    assert request_rig[0].end_index == 365 - 16
    assert len(request_record) == 1

def test_brazil():
    # A rig within the same year
    rig1 = Rig(datetime(2022, 1, 1), datetime(2022, 12, 31), -16.65, -49.22)
    record = Record([rig1])
    request_rig = rig1.to_precise_request()
    request_record = record.to_precise_request()

    # print(request_rig[0].get_uv_min('uvd_clear'))
    # print(request_rig[0].get_uv_max('uvd_clear'))
    # print(request_rig[0].get_uv_dose_clear())

    # No splitting should happen
    assert len(request_rig) == 1
    assert request_rig[0].filename == "UV_arxiv/uvdec2022_world.nc"
    assert request_rig[0].start_index == 0
    assert request_rig[0].end_index == 365
    assert len(request_record) == 1


# def test_jungfraujoch():
#     # A rig within the same year
#     rig1 = Rig(datetime(2020, 8, 1), datetime(2022, 8, 31), 46.55, 7.98)
#     rig2 = Rig(datetime(2020, 9, 1), datetime(2022, 9, 30), 46.55, 7.98)
#     rig3 = Rig(datetime(2020, 10, 1), datetime(2022, 10, 31), 46.55, 7.98)
#     rig4 = Rig(datetime(2020, 11, 1), datetime(2022, 11, 30), 46.55, 7.98)
#     rig5 = Rig(datetime(2020, 12, 1), datetime(2022, 12, 31), 46.55, 7.98)
#     rig6 = Rig(datetime(2021, 1, 1), datetime(2021, 1, 31), 46.55, 7.98)
#     rig7 = Rig(datetime(2021, 2, 1), datetime(2021, 2, 28), 46.55, 7.98)
#     rig8 = Rig(datetime(2021, 3, 1), datetime(2021, 3, 31), 46.55, 7.98)
#     rig9 = Rig(datetime(2021, 4, 1), datetime(2021, 4, 30), 46.55, 7.98)
#     rig10 = Rig(datetime(2021, 5, 1), datetime(2021, 5, 31), 46.55, 7.98)
#     # rig1 = Rig(datetime(2021, 6, 1), datetime(2021, 6, 30), 46.55, 7.98)
#     # rig1 = Rig(datetime(2021, 7, 1), datetime(2021, 7, 31), 46.55, 7.98)
#     # rig1 = Rig(datetime(2021, 8, 1), datetime(2021, 8, 31), 46.55, 7.98)
#     # rig1 = Rig(datetime(2021, 9, 1), datetime(2021, 9, 30), 46.55, 7.98)
#     # rig1 = Rig(datetime(2021, 10, 1), datetime(2021, 10, 31), 46.55, 7.98)
#     # rig1 = Rig(datetime(2021, 11, 1), datetime(2021, 11, 30), 46.55, 7.98)
#     # rig1 = Rig(datetime(2021, 12, 1), datetime(2021, 12, 31), 46.55, 7.98)
#     record = Record([rig1, rig2, rig3, rig4, rig5, rig6, rig7, rig8, rig9, rig10])
#     request_record = record.to_precise_request()
#
#     # print(request_rig[0].get_uv_min('uvd_clear'))
#     # print(request_rig[0].get_uv_max('uvd_clear'))
#     # for r in request_record[0:5]:
#     #     print(r.get_uv_dose_cloudy())
#
#     # No splitting should happen
#     assert len(request_record) == 10
#     assert request_rig[0].filename == "UV_arxiv/uvdec2022_world.nc"
#     assert request_rig[0].start_index == 0
#     assert request_rig[0].end_index == 31
#     assert len(request_record) == 10


def test_bern():
    # A rig within the same year
    rig1 = Rig(datetime(2022, 11, 25), datetime(2022, 11, 25), 46.95, 7.45)
    rig2 = Rig(datetime(2023, 8, 10), datetime(2023, 8, 10), 46.95, 7.45)
    record = Record([rig1, rig2])
    request_record = record.to_precise_request()

    # print(request_rig[0].get_uv_min('uvd_clear'))
    # print(request_rig[0].get_uv_max('uvd_clear'))
    print(len(request_record))
    for r in request_record:
        print(r.get_uv_dose_clear())

    # Splitting should happen
    assert len(request_record) == 6
    assert request_record[0].filename == "UV_arxiv/uvdec2021_world.nc"
    assert request_record[1].filename == "UV_arxiv/uvdec2022_world.nc"
    assert request_record[2].filename == "UV_arxiv/uvdec2022_world.nc"
    assert request_record[3].filename == "UV_arxiv/uvdec2023_world.nc"
    assert False

def test_multiple_years_record():
    # A rig that spans two years
    rig1 = Rig(datetime(2020, 6, 1), datetime(2020, 12, 15), 10.0, 50.0)
    rig2 = Rig(datetime(2021, 6, 1), datetime(2023, 3, 15), 20.0, 60.0)
    record = Record([rig1,rig2])
    request_rig2 = rig2.to_precise_request()
    request_record = record.to_precise_request()

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
    request_rig1 = rig1.to_precise_request()
    dose1 = request_rig1[0].get_uv_dose_clear()
    request_rig2 = rig2.to_precise_request()
    dose2 = request_rig2[0].get_uv_dose_clear()
    request_rig3 = rig3.to_precise_request()
    dose3 = request_rig3[0].get_uv_dose_clear()


    # No splitting should happen
    assert dose1 + dose2 == dose3