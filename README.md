# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version expands the starter catalog to 60 songs and uses an explainable content-based design to compare optional user preferences with song metadata. Five project-added attributes—release year, duration, instrumentalness, popularity, and liveness—add era, listening-context, vocal-content, discovery, and recording-environment signals while keeping every recommendation traceable to a weighted score breakdown.

---

## How The System Works

This simulator uses **content-based filtering**. It compares each song's descriptive features with one user's stated preferences, calculates a weighted score, sorts the songs from highest to lowest score, and returns the top results with an explanation.

The expanded recommendation design supports twelve preference-bearing features:

- `genre` and `mood`: 18% each
- `energy`: 11%
- `tempo_bpm`, `valence`, `danceability`, and `acousticness`: 7% each
- `instrumentalness`: 6%
- `liveness`, `release_year`, and `popularity`: 5% each
- `duration_seconds`: 4%

`preferred_genres` and `preferred_moods` are optional multi-select controls with an **Any** option. Exact category matches receive full credit, while a limited set of developer-defined related labels may receive partial credit. Numeric targets for the other ten features are optional advanced preferences. Unselected preferences are excluded, the remaining weights are renormalized, and at least one preference must be active. The proposed profile and formulas are documented in [Content-Based Recommender Dataset Analysis](content_based_recommender_dataset_analysis.md).

Recommendation explanations use progressive disclosure: they first describe the strongest matches in plain language, then identify which available features were **not considered** because the user did not select them. A technical score breakdown can be shown as optional detail. The displayed score is a deterministic compatibility score based only on active preferences; it is not a probability that the user will like the song.


### Feature origin

| Source | Features | How they are used |
|---|---|---|
| Starter project CSV | `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` | Identity, display, scoring, and analysis |
| Added during this project | `release_year`, `duration_seconds`, `instrumentalness`, `popularity`, `liveness` | Five additional scoring attributes for era, listening context, vocal content, discovery preference, and recording environment |

The five added columns and the 50 added songs contain synthetic values. Their structure is inspired by common music-catalog and audio-analysis metadata, but the values were not downloaded from or measured by Spotify, YouTube, or another streaming platform.

### Expected biases

This system may over-prioritize genre and mood because they receive 36% of the full score, causing it to miss strong songs that match the user's audio preferences but use different labels. Category counts also vary across the catalog. The limited related-category pairs are hand-written heuristics based on developer judgment; they are not relationships learned by AI or inferred from listening behavior. Musical relationships can vary by song, listener, culture, and listening context, so these rules may oversimplify compatibility.

For this simulator, the preferred baseline is exact genre and mood matching combined with numeric audio-feature similarity. This allows compatible songs to surface across category boundaries without requiring a subjective relationship rule. Related-category credit should remain optional, explicit, testable, and easy to disable. A production platform could instead learn relationships from sufficiently representative playlist, play, skip, like, and replay data.

### System flow

#### Quick data flow

[![Quick music recommender data flow](diagrams/recommender_quick_data_flow.svg)](diagrams/recommender_quick_data_flow.mmd)

#### Detailed scoring design

[![Content-based music recommender system flow](diagrams/recommender_system_flow.svg?v=5)](diagrams/recommender_system_flow.mmd)

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

Running `python -m src.main` with the default Pop/Happy profile (`target_energy=0.8`) produces:

```text
Loaded songs: 60

========================================================================
TOP MUSIC RECOMMENDATIONS
========================================================================

1. Sunrise City - Neon Echo
   Genre: Pop | Mood: Happy
   Match score: 99.5 / 100

   Why we recommended it:
     ✓ Genre: Pop matches your Pop preference
     ✓ Mood: Happy matches your Happy preference
     ✓ Energy: Very close to your target
       You requested 0.80; this song is 0.82

   Based on: Genre, mood, and energy
   Not considered: Tempo, valence, danceability, acousticness,
     instrumentalness, liveness, release year, duration, and popularity

   How the score was calculated:

   Factor             Match    Importance    Score points
   ------------------------------------------------------
   Genre              100%         38.3%            38.3
   Mood               100%         38.3%            38.3
   Energy              98%         23.4%            22.9
   ------------------------------------------------------
   Final score                                       99.5 / 100
   ---------------------------------------------------------------------

2. Rooftop Lights - Indigo Parade
   Genre: Indie Pop | Mood: Happy
   Match score: 79.9 / 100

   Why we recommended it:
     ~ Genre: Indie Pop is related to your Pop preference
     ✓ Mood: Happy matches your Happy preference
     ✓ Energy: Very close to your target
       You requested 0.80; this song is 0.76

   Based on: Genre, mood, and energy
   Not considered: Tempo, valence, danceability, acousticness,
     instrumentalness, liveness, release year, duration, and popularity

   How the score was calculated:

   Factor             Match    Importance    Score points
   ------------------------------------------------------
   Genre               50%         38.3%            19.1
   Mood               100%         38.3%            38.3
   Energy              96%         23.4%            22.5
   ------------------------------------------------------
   Final score                                       79.9 / 100
   ---------------------------------------------------------------------

3. Starlight Signal - Nova Seven
   Genre: Pop | Mood: Celebratory
   Match score: 79.0 / 100

   Why we recommended it:
     ✓ Genre: Pop matches your Pop preference
     ~ Mood: Celebratory is related to your Happy preference
     ✓ Energy: Close to your target
       You requested 0.80; this song is 0.88

   Based on: Genre, mood, and energy
   Not considered: Tempo, valence, danceability, acousticness,
     instrumentalness, liveness, release year, duration, and popularity

   How the score was calculated:

   Factor             Match    Importance    Score points
   ------------------------------------------------------
   Genre              100%         38.3%            38.3
   Mood                50%         38.3%            19.1
   Energy              92%         23.4%            21.5
   ------------------------------------------------------
   Final score                                       79.0 / 100
   ---------------------------------------------------------------------

4. Sunlit Mosaic - Harmony Market
   Genre: Indie Pop | Mood: Happy
   Match score: 77.6 / 100

   Why we recommended it:
     ~ Genre: Indie Pop is related to your Pop preference
     ✓ Mood: Happy matches your Happy preference
     ✓ Energy: Close to your target
       You requested 0.80; this song is 0.66

   Based on: Genre, mood, and energy
   Not considered: Tempo, valence, danceability, acousticness,
     instrumentalness, liveness, release year, duration, and popularity

   How the score was calculated:

   Factor             Match    Importance    Score points
   ------------------------------------------------------
   Genre               50%         38.3%            19.1
   Mood               100%         38.3%            38.3
   Energy              86%         23.4%            20.1
   ------------------------------------------------------
   Final score                                       77.6 / 100
   ---------------------------------------------------------------------

5. Lagos Sunrise - Kora Avenue
   Genre: World | Mood: Happy
   Match score: 61.7 / 100

   Why we recommended it:
     ✗ Genre: World does not match your Pop preference
     ✓ Mood: Happy matches your Happy preference
     ✓ Energy: Very close to your target
       You requested 0.80; this song is 0.80

   Based on: Genre, mood, and energy
   Not considered: Tempo, valence, danceability, acousticness,
     instrumentalness, liveness, release year, duration, and popularity

   How the score was calculated:

   Factor             Match    Importance    Score points
   ------------------------------------------------------
   Genre                0%         38.3%             0.0
   Mood               100%         38.3%            38.3
   Energy             100%         23.4%            23.4
   ------------------------------------------------------
   Final score                                       61.7 / 100
   ---------------------------------------------------------------------
```

Only genre, mood, and energy affect this run. Tempo, valence, danceability, acousticness, instrumentalness, liveness, release year, duration, and popularity are not considered because the default profile does not select them; they receive neither credit nor a penalty.

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
- Synthetic popularity is not evidence of real audience interest and may encourage mainstream-exposure bias if weighted too heavily.
- Synthetic liveness is not derived from audio analysis and should be treated as a classroom estimate rather than a measured probability.
- The model does not analyze lyrics, language, artist similarity, recency trends, or changes in a listener's taste over time.
- A small or uneven catalog limits recommendation diversity and may provide more choices for some categories than others.

These limitations are partially mitigated through visible score explanations, optional preferences, active-weight renormalization, category-level evaluation, and the ability to disable related-category rules. Additional technical detail appears in the [Content-Based Recommender Dataset Analysis](content_based_recommender_dataset_analysis.md) and `model_card.md`.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



