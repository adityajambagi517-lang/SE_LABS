import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# Branch coverage test cases: exercise both outcomes of each decision.
def test_speed_not_above_limit():
    assert speeding_fine(60, 60, "city") == 0

def test_speed_above_limit():
    assert speeding_fine(61, 60, "city") == 500

def test_school_zone_branch():
    assert speeding_fine(70, 60, "school") == 2000

def test_highway_zone_branch():
    assert speeding_fine(70, 60, "highway") == 1000

def test_other_zone_branch():
    assert speeding_fine(70, 60, "city") == 500

def test_excess_greater_than_40():
    assert speeding_fine(101, 60, "city") == 1500

def test_excess_equal_to_40_uses_middle_band():
    assert speeding_fine(100, 60, "city") == 1000

def test_excess_greater_than_20():
    assert speeding_fine(81, 60, "city") == 1000

def test_excess_equal_to_20_uses_base_band():
    assert speeding_fine(80, 60, "city") == 500

def test_points_at_least_12_commercial():
    assert license_action(12, True, False) == "revoke"

def test_points_at_least_12_noncommercial():
    assert license_action(12, False, False) == "suspend"

def test_points_between_8_and_11_repeat_offender():
    assert license_action(8, False, True) == "suspend"

def test_points_between_8_and_11_first_time():
    assert license_action(8, False, False) == "warning"

def test_points_between_4_and_7():
    assert license_action(4, False, False) == "notice"

def test_points_below_4():
    assert license_action(3, False, False) == "none"

def test_total_penalty_negative_branch():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([-10])

def test_total_penalty_nonnegative_branch():
    assert total_penalty([100, 200]) == 300

def test_total_penalty_above_cap_branch():
    assert total_penalty([7000, 5000]) == 10000

def test_total_penalty_at_cap_branch():
    assert total_penalty([5000, 5000]) == 10000

def test_total_penalty_below_cap_branch():
    assert total_penalty([1000, 2000]) == 3000
