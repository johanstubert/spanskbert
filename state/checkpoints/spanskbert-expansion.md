# Checkpoint: Spanskbert App Expansion

*Last updated: 2026-02-03*

---

## Session Summary
Built 2 new exercise apps (verb trainer + sentence practice) and added 9 new vocabulary categories across all 5 existing apps. Total app now has 7 exercise modes and 26 categories with ~290 words/phrases. Everything committed and pushed to GitHub.

## Key Decisions
- **Verb trainer uses two modes**: "Slumpad person" (random person per verb) and "Alla 6" (fill all 6 conjugation forms). This gives both quick practice and thorough drilling.
- **Sentence practice defaults to accent-lenient mode**: Since Johan is A0-A1, "Snall" mode (without accents) is the default. Strict mode available as toggle.
- **3-level hint system in sentence practice**: First word > word bank (shuffled) > show answer. Using "show answer" counts as wrong.
- **fill-blank-app.html as template**: Used as base for new apps (cleanest pattern, ~491 lines, text input + check flow).
- **9 new categories split into Situationer + Grundlaggande**: 5 situation-based (medico, deportes, tiempo, comida, escuela) + 4 basic vocab (cuerpo, ropa, profesiones, animales).
- **Each app gets data in its own format**: flashcard/quiz = `{es, sv}`, fill-blank = `{sentence, answer, translation}`, match-pairs = 6 `{es, sv}` pairs, sentence-builder = `{sentence, translation}`.
- **Blue gradient for verb trainer** (`#3498db -> #2980b9`), **teal for sentence practice** (`#1abc9c -> #16a085`).

## Current State

### Done
- verb-trainer-app.html created (32 verbs: 10 AR, 5 ER, 5 IR, 10 irregular, 2 reflexive) ✓
- sentence-practice-app.html created (7 categories, accent-tolerant, hints) ✓
- index.html updated with new mode cards + stats loading ✓
- 9 new categories added to flashcard-app.html ✓
- 9 new categories added to quiz-app.html ✓
- 9 new categories added to fill-blank-app.html ✓
- 9 new categories added to match-pairs-app.html ✓
- 9 new categories added to sentence-builder-app.html ✓
- index.html categoryData updated with new categories ✓
- Git commit b76516e pushed to main ✓

### In Progress
- Nothing

### Not Started
- Add more verbs (irregular verbs like dormir, pedir, jugar with stem changes)
- Add situation categories to sentence-practice-app (currently only grundlaggande)
- Lalia course material (folder is empty)
- Consider shared data file (currently each app embeds its own data)

## Key Context for Next Session
- **Tech stack**: Vanilla HTML/CSS/JS, no frameworks. Each app is a self-contained HTML file in `/docs/`.
- **Data is embedded in each HTML file** as JS constants (not loaded from external JSON).
- **localStorage keys**: `spanishFlashcards`, `spanishQuiz`, `spanishFillBlank`, `spanishMatchPairs`, `spanishSentenceBuilder`, `spanishVerbTrainer`, `spanishSentencePractice`.
- **Category keys must match across all apps** (e.g., `en_el_medico` is used identically in all 7 apps + index).
- **modulo-1-data.json** in `courses/sandra-gonzales/` has structured verb conjugation data that was sourced for the verb trainer.
- **Deployment**: Static files in `docs/`, served with `npx serve docs/`. Pushed to GitHub repo `johanstubert/spanskbert`.

## Next Actions
1. Add situation categories to sentence-practice-app.html (currently only has grundlaggande)
2. Add stem-changing irregular verbs (dormir, pedir, jugar, pensar, etc.) to verb trainer
3. Consider populating Lalia course material from PDFs
4. Consider extracting shared vocabulary data to a single JSON file to reduce duplication
