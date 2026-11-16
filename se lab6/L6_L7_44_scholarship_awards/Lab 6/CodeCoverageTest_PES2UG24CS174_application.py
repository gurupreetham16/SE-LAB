
import pytest
from scholarship_awards import award_amount, is_eligible, application_status


# Award amount test cases

def test_below_cutoff():
    assert award_amount("merit", 70, "low", False) == 0


def test_low_income_high_marks():
    assert award_amount("merit", 100, "low", False) == 4000


def test_high_income_high_marks():
    assert award_amount("sports", 90, "high", False) == 3000


def test_renewal_discount():
    assert award_amount("merit", 80, "low", True) == 1000


def test_unknown_category():
    with pytest.raises(ValueError):
        award_amount("science", 90, "low", False)


def test_negative_marks():
    with pytest.raises(ValueError):
        award_amount("merit", -5, "low", False)


# Eligibility test cases

def test_special_quota_eligible():
    assert is_eligible(60, 2, True) is True


def test_regular_eligible():
    assert is_eligible(85, 1, False) is True


def test_low_attendance():
    assert is_eligible(70, 0, False) is False


# Application status test cases

def test_application_open():
    assert application_status(25, False, False) == "open"


def test_application_closing():
    assert application_status(10, False, False) == "closing"


def test_application_closed():
    assert application_status(4, False, False) == "closed"
