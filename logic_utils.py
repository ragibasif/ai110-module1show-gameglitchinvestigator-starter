def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: Hard was returning 1–50, narrower than Normal's 1–100. AI (Claude) identified
    # the inversion by comparing the three ranges; fix confirmed by switching to Hard in
    # the sidebar and checking the "Range:" caption updated to 1 to 500.
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if not raw:
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: Messages were inverted — "Too High" told the player to go higher. AI (Claude)
    # spotted the swap by reading the return values; fix verified by running pytest
    # (test_too_high_hint_says_lower / test_too_low_hint_says_higher) and manually
    # submitting an out-of-range guess in the live Streamlit app.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
