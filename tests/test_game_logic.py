from logic_utils import check_guess, get_range_for_difficulty


# --- check_guess ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug 1 fix: hint messages were inverted ---

def test_too_high_hint_says_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message.upper()

def test_too_low_hint_says_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message.upper()


# --- Bug 3 fix: Hard difficulty range was narrower than Normal ---

def test_hard_range_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high
