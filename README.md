# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This simulator uses **content-based filtering**. It compares each song's descriptive features with one user's stated preferences, calculates a weighted score, sorts the songs from highest to lowest score, and returns the top results with an explanation.

The expanded recommendation design supports ten preference-bearing features:

- `genre` and `mood`: 20% each
- `energy`: 12%
- `tempo_bpm`, `valence`, `danceability`, and `acousticness`: 8% each
- `instrumentalness`: 6%
- `release_year` and `duration_seconds`: 5% each

`preferred_genres` and `preferred_moods` are optional multi-select controls with an **Any** option. Exact category matches receive full credit, while a limited set of developer-defined related labels may receive partial credit. Numeric targets for the other eight features are optional advanced preferences. Unselected preferences are excluded, the remaining weights are renormalized, and at least one preference must be active. The proposed profile and formulas are documented in [Content-Based Recommender Dataset Analysis](content_based_recommender_dataset_analysis.md).

### Feature origin

| Source | Features | How they are used |
|---|---|---|
| Starter project CSV | `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` | Identity, display, scoring, and analysis |
| Added during this project | `release_year`, `duration_seconds`, `instrumentalness` | Expanded optional recommendation preferences and deeper analysis |

The three added columns and the 50 added songs contain synthetic values. Their structure is inspired by common music-catalog and audio-analysis metadata, but the values were not downloaded from or measured by Spotify, YouTube, or another streaming platform. The added rows were consolidated into a shared vocabulary, producing 13 genres and 9 moods with multiple songs per category; the original 10 starter rows were not changed.

### Expected biases

This system may over-prioritize genre and mood because they receive 40% of the full score, causing it to miss strong songs that match the user's audio preferences but use different labels. Category counts also vary across the catalog. The limited related-category pairs are hand-written heuristics based on developer judgment; they are not relationships learned by AI or inferred from listening behavior. Musical relationships can vary by song, listener, culture, and listening context, so these rules may oversimplify compatibility.

For this simulator, the preferred baseline is exact genre and mood matching combined with numeric audio-feature similarity. This allows compatible songs to surface across category boundaries without requiring a subjective relationship rule. Related-category credit should remain optional, explicit, testable, and easy to disable. A production platform could instead learn relationships from sufficiently representative playlist, play, skip, like, and replay data.

### System flow

#### Quick data flow

[![Quick music recommender data flow](diagrams/recommender_quick_data_flow.svg)](diagrams/recommender_quick_data_flow.mmd)

#### Detailed scoring design

[![Content-based music recommender system flow](diagrams/recommender_system_flow.svg?v=4)](diagrams/recommender_system_flow.mmd)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

- The catalog contains only 60 songs, and most added metadata values are synthetic rather than platform measurements.
- The system has no behavioral feedback such as plays, skips, likes, replays, or playlist co-occurrence, so it cannot learn preferences automatically.
- Related genre and mood pairs reflect developer assumptions and may not represent every listener or cultural context.
- Static feature weights may overemphasize genre and mood or count correlated signals, such as energy and tempo, more than once.
- The model does not analyze lyrics, language, artist similarity, popularity, recency trends, or changes in a listener's taste over time.
- A small or uneven catalog limits recommendation diversity and may provide more choices for some categories than others.

These limitations are partially mitigated through visible score explanations, optional preferences, active-weight renormalization, category-level evaluation, and the ability to disable related-category rules. Additional technical detail appears in the [Content-Based Recommender Dataset Analysis](content_based_recommender_dataset_analysis.md) and `model_card.md`.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



