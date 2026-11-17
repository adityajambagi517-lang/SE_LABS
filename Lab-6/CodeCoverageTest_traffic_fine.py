import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# Line coverage test cases
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0

def test_school_zone_fine():
    assert speeding_fine(70, 60, "school") == 2000

def test_highway_fine():
    assert speeding_fine(70, 60, "highway") == 1000

def test_city_fine():
    assert speeding_fine(70, 60, "city") == 500

def test_excess_over_40_school():
    assert speeding_fine(105, 60, "school") == 6000

def test_excess_over_20_highway():
    assert speeding_fine(85, 60, "highway") == 2000

def test_license_clean_record():
    assert license_action(2, False, False) == "none"

def test_license_notice():
    assert license_action(4, False, False) == "notice"

def test_license_warning():
    assert license_action(8, False, False) == "warning"

def test_license_suspend_repeat():
    assert license_action(8, False, True) == "suspend"

def test_license_suspend_noncommercial():
    assert license_action(12, False, False) == "suspend"

def test_license_revoke_commercial():
    assert license_action(12, True, False) == "revoke"

def test_total_penalty_normal():
    assert total_penalty([500, 1000, 1500]) == 3000

def test_total_penalty_cap():
    assert total_penalty([6000, 6000]) == 10000

def test_total_penalty_negative_raises():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([500, -1])
