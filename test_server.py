import pytest
from datetime import datetime, timedelta
from server import get_avg_hr, get_int_ave, is_tachy, \
    validate_newp_req, validate_hr_req


@pytest.mark.parametrize("hr_list, expected", [
    ([120, 30, 45], (120+30+45)/3),
    ([], 'No heart rates recorded')

])
def test_get_avg_hr(hr_list, expected):
    assert get_avg_hr(hr_list) == expected


@pytest.mark.parametrize("times, hrs, interval, expected", [
    ([datetime.now() - timedelta(days=1)], [130], "2018-03-09 "
                                                  "11:00:36.372339", 130),
    ([datetime.now() - timedelta(weeks=50)], [130], "2018-03-09 "
                                                    "11:00:36.372339",
     'No heart rates recorded during that time interval'),
    ([datetime.now() - timedelta(days=1), datetime.now() - timedelta(days=3),
      datetime.now() - timedelta(days=4)], [130, 75, 90], "2018-03-09 "
                                                          "11:00:36.372339",
     (130+75+90)/3),
])
def test_get_int_ave(times, hrs, interval, expected):
    assert get_int_ave(times, hrs, interval) == expected


@pytest.mark.parametrize("age, hr, expected", [
    (0, 40, 'Patient is too young to detect tachycardia '
            'with this program'),
    (1, 160, 'Tachycardic'),
    (3, 100, 'Non-Tachycardic'),
    (6, 134, 'Tachycardic'),
    (9, 120, 'Non-Tachycardic'),
    (14, 119, 'Tachycardic'),
    (50, 100, 'Tachycardic'),
])
def test_tachy(age, hr, expected):
    assert is_tachy(age, hr) == expected


def test_validate_newp_req():
    test1 = {
        "patient_id": 1,
        "attending_email": "email@test.com",
        "user_age": '57'
    }
    assert validate_newp_req(test1) is True
    test2 = {
        "patient_id": 'j'
    }
    assert validate_newp_req(test2) is False
    test3 = {
        "patient_id": '3',
        "attending_email": 'notanemail'
    }
    assert validate_newp_req(test3) is False
    test4 = {
        "patient_id": '39',
        "attending_email": 'fake@email.com',
        "user_age": 'old'
    }
    assert validate_newp_req(test4) is False


def test_validate_hr_req():
    test1 = {
        "patient_id": 'g'
    }
    assert validate_hr_req(test1) is False
    test2 = {
        "patient_id": '3',
        "heart_rate": 'lol'
    }
    assert validate_hr_req(test2) is False
    test3 = {
        "patient_id": '90994',
        "heart_rate": '900'
    }
    assert validate_hr_req(test3) is True
