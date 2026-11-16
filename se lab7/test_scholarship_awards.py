import math

from hypothesis import given, settings, strategies as st
from scholarship_awards import parse_applicant, marks_average, payable_award


# ---------- Crash-resistance (fuzz) tests ----------

@given(st.text() | st.none())
def test_parse_applicant_no_crash(s):
    try:
        parse_applicant(s)
    except Exception as e:
        assert False, f"parse_applicant crashed with: {e!r}"


@given(st.text() | st.none())
def test_marks_average_no_crash(s):
    try:
        marks_average(s)
    except Exception as e:
        assert False, f"marks_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_award_no_crash(s):
    try:
        payable_award(s)
    except Exception as e:
        assert False, f"payable_award crashed with: {e!r}"


# ---------- Extra fuzzing on non-string types ----------

@given(st.one_of(st.integers(), st.floats(), st.lists(st.integers()), st.binary(), st.booleans()))
def test_all_functions_survive_non_strings(x):
    for fn in (parse_applicant, marks_average, payable_award):
        try:
            fn(x)
        except Exception as e:
            assert False, f"{fn.__name__} crashed on {x!r} with: {e!r}"


# ---------- Correctness properties on well-formed input ----------

@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=20))
def test_marks_average_is_true_mean_and_in_range(marks):
    result = marks_average(",".join(map(str, marks)))
    assert result is not None
    assert min(marks) <= result <= max(marks)
    assert math.isclose(result, sum(marks) / len(marks), abs_tol=0.01)


@given(st.text(alphabet=st.characters(whitelist_categories=("Ll", "Lu")), min_size=1, max_size=15),
       st.integers(min_value=0, max_value=100))
def test_parse_applicant_valid_roundtrip(category, marks):
    result = parse_applicant(f"{category}:{marks}")
    assert result == (category.strip().title(), float(marks))


@given(st.integers(min_value=0, max_value=10**7), st.integers(min_value=0, max_value=10**7))
def test_payable_award_never_negative_and_finite(award, deduction):
    result = payable_award(f"{award}|{deduction}")
    assert result is not None
    assert math.isfinite(result) and result >= 0
    assert math.isclose(result, max(award * 1.18 - deduction, 0), abs_tol=0.01)


@given(st.one_of(st.just(float("nan")), st.just(float("inf")), st.just(float("-inf"))))
def test_non_finite_numbers_rejected(v):
    assert payable_award(f"{v}|0") is None
    assert payable_award(f"100|{v}") is None
    assert parse_applicant(f"merit:{v}") is None
    assert marks_average(f"50,{v}") is None
