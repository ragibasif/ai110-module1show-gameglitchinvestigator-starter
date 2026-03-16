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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
