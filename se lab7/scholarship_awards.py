"""Scholarship awards helpers (hardened after fuzz testing with Hypothesis).

Design: every function validates its input and returns None for anything
invalid (wrong type, malformed text, NaN/inf, out-of-range) instead of raising.
"""
import math

MIN_MARK = 0.0
MAX_MARK = 100.0
TAX_MULTIPLIER = 1.18  # 18% added on the award amount


def _to_finite_float(token):
    """Parse a string to a finite float, or return None."""
    try:
        value = float(token)
    except (ValueError, OverflowError):
        return None
    return value if math.isfinite(value) else None


def _valid_mark(value):
    return value is not None and MIN_MARK <= value <= MAX_MARK


def parse_applicant(text):
    """'merit:82' -> ('Merit', 82.0); None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split(":")
    if len(parts) != 2:
        return None
    category = parts[0].strip()
    marks = _to_finite_float(parts[1])
    if not category or not _valid_mark(marks):
        return None
    return category.title(), marks


def marks_average(marks_csv):
    """'72,85,90' -> 82.33 (true mean, 2 dp); None if invalid or empty."""
    if not isinstance(marks_csv, str):
        return None
    values = []
    for token in marks_csv.split(","):
        mark = _to_finite_float(token)
        if not _valid_mark(mark):
            return None
        values.append(mark)
    # split() always yields >=1 token, and empty tokens fail parsing above,
    # so values is never empty here (no ZeroDivisionError).
    return round(sum(values) / len(values), 2)


def payable_award(text):
    """'5000|500' -> 5400.0 (award * 1.18 - deduction, floored at 0); None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split("|")
    if len(parts) != 2:
        return None
    award = _to_finite_float(parts[0])
    deduction = _to_finite_float(parts[1])
    if award is None or deduction is None or award < 0 or deduction < 0:
        return None
    total = award * TAX_MULTIPLIER - deduction
    if not math.isfinite(total):  # e.g. 1e308 * 1.18 overflows to inf
        return None
    return round(max(total, 0.0), 2)


def _show(result):
    print("Invalid input" if result is None else result)


def main():
    print("==== Running parse_applicant ====")
    user_input = input("Enter category:marks (e.g. merit:82): ")
    print("Category and Marks:", end=" ")
    _show(parse_applicant(user_input))

    print("\n==== Running marks_average ====")
    user_input = input("Enter marks as CSV (e.g. 72,85,90): ")
    print("Average Marks:", end=" ")
    _show(marks_average(user_input))

    print("\n==== Running payable_award ====")
    user_input = input("Enter award|deduction (e.g. 5000|500): ")
    print("Payable Award:", end=" ")
    _show(payable_award(user_input))


if __name__ == "__main__":
    main()
