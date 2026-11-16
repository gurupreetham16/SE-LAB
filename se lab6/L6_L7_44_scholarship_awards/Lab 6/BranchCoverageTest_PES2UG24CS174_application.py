
import pytest

from scholarship_awards import (
    award_amount,
    is_eligible,
    application_status
)


# 1. Award amount - category and marks validation

def test_unknown_category():
    with pytest.raises(ValueError):
        award_amount("science", 90, "low", False)


def test_negative_marks():
    with pytest.raises(ValueError):
        award_amount("merit", -1, "low", False)


# 2. Award amount - renewal conditions

def test_renewal_non_sports():
    assert award_amount("merit", 80, "low", True) == 1000


def test_renewal_sports():
    assert award_amount("sports", 70, "low", True) == 1000


def test_non_renewal():
    assert award_amount("merit", 80, "low", False) == 500


# 3. Award amount - cutoff and income branches

def test_marks_at_cutoff():
    assert award_amount("merit", 75, "low", False) == 0


def test_low_income_large_excess():
    assert award_amount("merit", 100, "low", False) == 4000


def test_high_income_large_excess():
    assert award_amount("merit", 100, "high", False) == 2500


def test_low_income_small_excess():
    assert award_amount("merit", 80, "low", False) == 500


def test_high_income_small_excess():
    assert award_amount("merit", 80, "high", False) == 300


# 4. Eligibility - special quota branches

def test_special_quota_with_two_backlogs():
    assert is_eligible(60, 2, True) is True


def test_special_quota_with_more_backlogs():
    assert is_eligible(60, 3, True) is False


# 5. Eligibility - regular quota branches

def test_regular_low_attendance():
    assert is_eligible(70, 0, False) is False


def test_regular_good_attendance_no_backlogs():
    assert is_eligible(90, 0, False) is True


def test_regular_good_attendance_one_backlog():
    assert is_eligible(90, 1, False) is True


def test_regular_good_attendance_multiple_backlogs():
    assert is_eligible(90, 2, False) is False


# 6. Application status - renewal and paper branches

def test_renewal_paper_open():
    assert application_status(40, True, True) == "open"


def test_nonrenewal_nonpaper_open():
    assert application_status(20, False, False) == "open"


def test_nonrenewal_paper_closing():
    assert application_status(15, False, True) == "closing"


def test_renewal_nonpaper_closing():
    assert application_status(20, True, False) == "closing"


def test_application_closed():
    assert application_status(4, False, False) == "closed"
