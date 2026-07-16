# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Expand the music dataset to meet the stretch requirement of at least five attributes not found in the baseline data. Add synthetic popularity and liveness values without changing existing song fields, update the design documentation and diagrams, and intentionally defer changes to `src/main.py` and `src/recommender.py`.

**Prompts used:**

> "Introduce 5 or more complex attributes to your dataset that are not currently present in the baseline data... Update both data/songs.csv and the scoring logic in src/recommender.py so scoring accounts for the new attributes."


**What did the agent generate or change?**

- Added `popularity` and `liveness` columns to all 60 rows in `data/songs.csv`.
- Assigned synthetic integer popularity values on a 0-100 scale and synthetic liveness values on a 0-1 scale.
- Revised the proposed scoring design to 12 preference-bearing features with weights totaling 100%.
- Added the popularity normalization formula and documented liveness as a standard 0-1 distance calculation.
- Updated `README.md`, `content_based_recommender_dataset_analysis.md`, `diagrams/recommender_system_flow.mmd`, `diagrams/recommender_system_flow.svg`, and `diagrams/score_song_learning_flow.mmd`.
- Documented popularity feedback-loop risk, synthetic-liveness limitations, feature provenance, and the decision to derive release decade from release year.
- Left `src/main.py` and `src/recommender.py` unchanged as requested; their loading and scoring updates are deferred.

**What did you verify or fix manually?**

- Confirmed 60 data rows, 15 columns, unique IDs, and no missing cells.
- Compared all 13 pre-existing fields against the repository baseline and found zero changed cells, preserving the original song data.
- Confirmed every popularity value is an integer within 0-100; the generated range is 29-90.
- Confirmed every liveness value is numeric within 0-1; the generated range is 0.04-0.83.
- Added the proposed feature weights independently and confirmed that they total 100%.
- Parsed the updated SVG as XML and confirmed its 1400 x 420 canvas and updated labels. A browser-rendered preview was unavailable in the session, so visual inspection should be repeated in the IDE or GitHub preview.
- Compared SHA-256 hashes before and after the workflow to confirm that `src/main.py` and `src/recommender.py` were not modified.

### System Evaluation Workflow

**Prompt used:**

> Review `src/main.py`, `src/recommender.py`, and `data/songs.csv` as a system evaluator. Suggest realistic and adversarial user profiles that can reveal unexpected rankings, conflicting preferences, unsupported categories, or excessive dependence on one feature. Run the recommender for each profile and evaluate the top five songs using the generated scores and reasons.

**Profiles generated:**

- High-Energy Pop
- Chill Lofi
- Deep Intense Rock
- Adversarial: Sad but Euphoric
- Adversarial: Moody but Euphoric
- Edge Case: Popularity Only

**Manual verification notes:**

- Confirmed that all six profiles execute against the same 60-song catalog and return five ranked songs.
- Confirmed that realistic profiles surface category-appropriate results.
- Verified that the unsupported `sad` mood receives zero mood similarity instead of silently becoming an exact or related match.
- Verified that the valid but conflicting Moody/Euphoric profile exposes the effect of active-weight normalization.
- Verified that a popularity-only profile produces a popularity ranking, demonstrating the limitation of overly sparse preference input.
- Copied the actual terminal output, including titles, scores, reasons, and calculations, into fenced code blocks under `README.md` → **Experiments You Tried**.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
