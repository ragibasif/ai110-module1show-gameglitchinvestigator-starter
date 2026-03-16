# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When the game first ran it appeared functional — you could enter a guess and get feedback — but the responses were actively misleading and the difficulty settings were wrong. Playing revealed four concrete bugs:

**Bug 1 — Hints were backwards**
- **Expected:** Guessing too high should say "Go LOWER" and guessing too low should say "Go HIGHER".
- **What actually happened:** The logic in `check_guess` was inverted — guessing too high returned "📈 Go HIGHER!" and guessing too low returned "📉 Go LOWER!", steering the player in the wrong direction every single time.

**Bug 2 — Hints broke on every other guess**
- **Expected:** The comparison between the guess and the secret number should always work correctly regardless of how many guesses have been made.
- **What actually happened:** On every even-numbered attempt, `app.py` converted the secret number to a string before comparing (`secret = str(st.session_state.secret)`). This caused Python to use lexicographic (alphabetical) ordering instead of numeric ordering, so e.g. the string `"9"` compared as greater than `"10"`, producing wrong hints on alternating turns.

**Bug 3 — Hard mode was easier than Normal**
- **Expected:** Higher difficulty should mean a wider range of possible numbers and therefore a harder game (Easy: 1–20, Normal: 1–100, Hard: 1–1000 or similar).
- **What actually happened:** `get_range_for_difficulty` returned `1–50` for Hard and `1–100` for Normal, making Hard mode easier than Normal since there were fewer possible values to search through.

**Bug 4 — Starting a new game left you locked out**
- **Expected:** Clicking "New Game" should fully reset the game so you can play again immediately.
- **What actually happened:** The "New Game" button reset the secret number and attempt count but never reset `st.session_state.status`. After winning or losing, `status` stayed as `"won"` or `"lost"`, so the `st.stop()` check triggered immediately after the rerun and the player could not make any guesses.

---

## 2. How did you use AI as a teammate?

I used Claude (via Claude Code) as my AI teammate throughout this project.

**Correct AI suggestion — refactoring logic into `logic_utils.py`**
Claude suggested moving all four game logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` and into a separate `logic_utils.py` module, then importing them back with a single line. This was correct: `app.py` shrank from ~70 lines of mixed logic and UI code to a clean file that only handles Streamlit rendering. I verified the result by running `streamlit run app.py` and confirming the game still launched and responded to guesses exactly as before, and by running `pytest` to confirm all six tests passed after the move.

**Incorrect/misleading AI suggestion — overly complex test assertions**
When generating the initial pytest cases for the inverted hint bug, Claude wrote tests that called `.upper()` on the message string and checked for substrings like `"LOWER"` or `"HIGHER"`. While technically correct, this was misleading for a beginner: it made a simple outcome check look complicated and fragile (it would silently break if the emoji or wording changed). The simpler and more robust approach is to just unpack the tuple and assert on the outcome string — `assert outcome == "Too High"` — which tests the game logic without tying the test to the exact wording of a UI message. I verified this by rewriting the tests in the simpler style and confirming they still caught the bug (all four bug-targeted tests failed before the fix, all six passed after).

---

## 3. Debugging and testing your fixes

A bug was only considered fixed when two things were true: the relevant pytest test turned from red to green, and the correct behavior was visible in the running Streamlit app.

For Bug 1 (inverted hints), the pytest test `test_too_high_hint_says_lower` called `check_guess(60, 50)` and asserted `"LOWER"` appeared in the message. Before the fix it failed with `AssertionError: got '📈 Go HIGHER!'`; after swapping the two return strings the test passed. I then opened the live app, checked the secret in the Debug Info panel, submitted a guess above it, and confirmed the hint now read `📉 Go LOWER!` rather than sending me in the wrong direction.

For Bug 3 (Hard range), `test_hard_range_wider_than_normal` asserted `hard_high > normal_high`. Before the fix it failed with `AssertionError: 50 > 100`; after changing Hard to return `1–500` it passed. I verified in the app by selecting Hard in the sidebar and checking that the `Range:` caption updated to `1 to 500`.

Claude helped design the initial test structure (showing how to unpack the tuple return value and what edge cases to cover), but the final, simplified test style — asserting directly on the outcome string — came from recognising that simpler assertions are easier to read and harder to accidentally break.

---

## 4. What did you learn about Streamlit and state?

Every time a user interacts with a Streamlit widget — clicking a button, changing a dropdown — Streamlit reruns the entire Python script from top to bottom. In the original app, `random.randint(low, high)` was called unconditionally at the top level, so every button click generated a brand-new secret number and wiped out any progress the player had made.

If I were explaining this to a friend: imagine every button click in a web app refreshed the whole page and re-ran all the setup code. That would be chaos — your form inputs would disappear, your score would reset, everything would start over. Streamlit's `st.session_state` is a dictionary that survives those reruns, so you can store values there (like the secret number or the current score) and they persist across clicks.

The fix was wrapping the secret generation in a `if "secret" not in st.session_state:` guard. That way `random.randint` only runs once — the very first time the page loads — and every subsequent rerun just reads the already-stored value instead of replacing it.

---

## 5. Looking ahead: your developer habits

**Habit to keep — write a failing test before touching the fix.**
On this project I added FIXME comments, wrote pytest cases that explicitly failed against the broken code, and only then made the code change. Seeing the test go from red to green gave me concrete proof the fix actually worked, rather than just assuming it did. I want to carry that habit into future labs: don't claim something is fixed until a test says so.

**One thing I'd do differently — ask the AI to explain its reasoning before accepting a suggestion.**
I accepted the first test structure Claude produced (substring checks on the message string) without questioning it. When I was told to simplify, the better approach was obvious in hindsight. Next time I'll ask "why did you choose this approach and what are the trade-offs?" before running with any non-trivial suggestion.

**How this changed my thinking about AI-generated code.**
Before this project I assumed AI-generated code was either correct or obviously broken. What I actually found was subtler: the code ran without errors, looked reasonable at first glance, and only revealed its bugs when I played it carefully or wrote tests against it. AI code needs the same skeptical review you'd give any code from a new colleague — running it is not the same as verifying it.
