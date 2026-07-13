# Content-Based Recommender Dataset Analysis

## Purpose

This document examines `data/songs.csv` from a system-design perspective and identifies which attributes are effective for a simple content-based music recommender. The analysis is specific to the current simulator, its ten-song catalog, and the existing `Song` and `UserProfile` classes.

## Dataset Overview

The dataset contains **10 songs and 11 attributes**.

| Attribute | Type | Observed values or range | Recommended role |
|---|---|---|---|
| `id` | Integer identifier | 1-10 | Identity only; do not score |
| `title` | Text metadata | Unique song titles | Display and explanation only |
| `artist` | Categorical metadata | 8 artists | Optional preference/diversity signal |
| `genre` | Categorical feature | 7 labels | Strong scoring feature |
| `mood` | Categorical feature | 6 labels | Strong scoring feature |
| `energy` | Numeric feature | 0.28-0.93 | Strong scoring feature |
| `tempo_bpm` | Numeric feature | 60-152 BPM | Useful optional feature |
| `valence` | Numeric feature | 0.48-0.84 | Useful optional feature |
| `danceability` | Numeric feature | 0.41-0.88 | Useful optional feature |
| `acousticness` | Numeric feature | 0.05-0.92 | Strong scoring feature |

Numeric averages in this catalog are:

- Energy: **0.599**
- Tempo: **101.6 BPM**
- Valence: **0.650**
- Danceability: **0.663**
- Acousticness: **0.506**

## Dataset Coverage

### Genre distribution

| Genre | Songs |
|---|---:|
| lofi | 3 |
| pop | 2 |
| ambient | 1 |
| indie pop | 1 |
| jazz | 1 |
| rock | 1 |
| synthwave | 1 |

### Mood distribution

| Mood | Songs |
|---|---:|
| chill | 3 |
| happy | 2 |
| intense | 2 |
| focused | 1 |
| moody | 1 |
| relaxed | 1 |

The catalog is small and uneven. Lofi and chill are more heavily represented than most alternatives, so profiles matching those labels have more candidates. A user who prefers rock, jazz, ambient, or synthwave can receive only one exact genre match. This means a recommender based only on exact categorical matches would often produce weak or repetitive results.

## Attribute Effectiveness

### 1. Genre: highly effective

Genre is easy for users to understand and provides a strong high-level indication of taste. It should receive a meaningful score bonus when the song genre matches the user's favorite genre.

The system should normalize values by trimming whitespace and converting text to lowercase. It should also decide how related labels are treated. For example, an exact-match algorithm considers `pop` and `indie pop` different even though they are related. A future version could use a small genre-family map so that `indie pop` receives partial credit for a `pop` preference.

**Recommendation:** Use in V1 as an exact match, with optional partial matching added later.

### 2. Mood: highly effective

Mood directly represents the listening experience a user may want. It is particularly useful when music is selected for studying, exercising, relaxing, or improving one's mood.

As with genre, the current labels are exact categories. `chill` and `relaxed` may be semantically close but receive no shared credit in a simple exact-match design. A mood-family mapping could later assign partial similarity between related labels.

**Recommendation:** Use in V1 as an exact match.

### 3. Energy: highly effective

Energy is numeric and has good separation across the catalog, from 0.28 to 0.93. It supports more precise matching than a category because the system can reward closeness rather than require equality.

A simple similarity calculation is:

```text
energy_similarity = 1 - abs(user_target_energy - song_energy)
```

Because both values use a 0-1 scale, the result is also between 0 and 1. A song at 0.82 energy is therefore a closer match to a target of 0.80 than a song at 0.40.

**Recommendation:** Use in V1 as a continuous similarity score.

### 4. Acousticness: effective with careful profile mapping

Acousticness has a wide range, from 0.05 to 0.92, so it clearly distinguishes electronic or heavily produced tracks from acoustic tracks. The current `UserProfile` represents the preference as the Boolean `likes_acoustic`, while songs use a continuous 0-1 value.

For a simple implementation, map `likes_acoustic=True` to a high target such as 0.8 and `False` to a low target such as 0.2, then score numeric closeness. This is more informative than using an arbitrary hard cutoff.

The Boolean profile is still restrictive: a user who does not specifically prefer acoustic music may not actively dislike it. A later version should replace it with `target_acousticness: float` or make this preference optional.

**Recommendation:** Use in V1, but give it less weight than genre, mood, and energy.

### 5. Tempo: useful after expanding the user profile

Tempo ranges from 60 to 152 BPM and can distinguish slow ambient or lofi music from faster workout or rock tracks. However, the existing `UserProfile` has no target tempo, so the recommender currently has nothing meaningful to compare it with. Inferring a user's desired tempo from energy would duplicate information and could make the score appear more confident without adding a real preference.

If `target_tempo_bpm` is added later, similarity can be based on normalized distance. The normalization must prevent tempo from dominating merely because it uses a much larger numeric scale than the 0-1 features.

**Recommendation:** Exclude from V1 scoring; add when the profile accepts a tempo preference.

### 6. Valence: useful after expanding the user profile

Valence estimates musical positivity. It could distinguish cheerful from darker-sounding tracks, but its observed range is fairly narrow at 0.48-0.84 and the current profile does not store a valence target. It may also overlap conceptually with labels such as `happy` and `moody`.

**Recommendation:** Exclude from V1. Consider it later as a continuous alternative or supplement to mood, while avoiding double-counting the same concept.

### 7. Danceability: useful after expanding the user profile

Danceability ranges from 0.41 to 0.88 and could improve party, exercise, or movement-focused recommendations. It is not represented in the current user profile.

**Recommendation:** Exclude from V1. Add an optional danceability preference in an expanded simulator.

### 8. Artist: limited as a scoring feature

Artist is useful metadata, but only Neon Echo and LoRoom appear more than once. Exact artist matching would be unreliable in this small catalog and could over-recommend familiar artists. Artist is more useful for controlling diversity, such as preventing the top results from being dominated by one artist.

**Recommendation:** Do not include in the core V1 score. Use for tie-breaking, explanations, or a one-song-per-artist diversity rule.

### 9. ID and title: not recommendation features

`id` identifies a record, and `title` presents it to the user. Neither describes musical similarity. Scoring them would introduce arbitrary behavior.

**Recommendation:** Use only for identity, display, logging, and explanations.

## Recommended Simple Scoring Design

The best V1 design uses only features that have a corresponding user preference:

| Signal | Weight | Similarity calculation |
|---|---:|---|
| Genre | 30% | 1 for exact match; otherwise 0 |
| Mood | 30% | 1 for exact match; otherwise 0 |
| Energy | 25% | `1 - abs(target_energy - energy)` |
| Acousticness | 15% | `1 - abs(acoustic_target - acousticness)` |

```text
final_score =
    0.30 * genre_match
  + 0.30 * mood_match
  + 0.25 * energy_similarity
  + 0.15 * acoustic_similarity
```

This produces a score between 0 and 1. The categorical weights make explicit genre and mood choices important, while the continuous features help rank songs that have the same number of category matches.

These weights are reasonable starting assumptions, not learned facts. They should be tested with multiple profiles and adjusted based on whether the top recommendations appear sensible. They should also be stored as named constants so experiments remain easy to understand.

## Ranking and Explanation Flow

```text
UserProfile
    -> normalize preference values
    -> calculate four similarities for every song
    -> combine similarities using weights
    -> sort by descending score
    -> apply artist diversity rule if desired
    -> return top k songs with explanations
```

An explanation should mention the strongest genuine matches, for example:

> Recommended because it matches your pop and happy preferences and its 0.82 energy is close to your 0.80 target.

The explanation should not claim that a feature matched when it merely had a small effect on the numeric score.

## Design Risks and Mitigations

### Small catalog

Ten songs are sufficient for a classroom simulation but too few for reliable personalization. Results will often contain songs that do not closely match the profile simply because there are no better candidates.

**Mitigation:** Show match scores and explanations, and avoid presenting the results as predictions of what the user will definitely like.

### Representation imbalance

Lofi/chill profiles have more exact-match options than profiles for genres and moods represented once. This can create an experience-quality difference between users.

**Mitigation:** Expand underrepresented categories and evaluate recommendation quality separately for different profiles.

### Overspecialization

Exact genre and mood rewards can repeatedly return similar tracks.

**Mitigation:** Reserve one top-k position for a near match, add partial category similarity, or rerank results for genre and artist diversity.

### Double-counting related features

Mood and valence can represent similar emotional qualities; energy and tempo can also be related. Giving all of them large independent weights may overemphasize one dimension of taste.

**Mitigation:** Start with the four-feature V1 design. Add a feature only when it represents an explicit user preference and evaluation shows that it improves ranking.

### Missing preference handling

Future user profiles may omit a preference. Treating a missing value as zero would incorrectly mean the user wants the lowest possible value.

**Mitigation:** Skip missing features and renormalize the weights of the preferences that are present.

## Recommended Development Path

1. Implement the four-feature V1 score using genre, mood, energy, and acousticness.
2. Return a score breakdown so each recommendation can be inspected and explained.
3. Test contrasting profiles, including happy pop, chill lofi, intense rock, and acoustic jazz.
4. Check whether each profile has enough suitable candidates and document catalog gaps.
5. Add optional tempo, valence, or danceability preferences one at a time and compare the rankings before keeping them.
6. Expand the dataset before attempting complex similarity models or learning weights from behavior.

## Conclusion

For the current simulator, **genre, mood, energy, and acousticness** form the most effective simple content-based feature set because the dataset contains them and the existing `UserProfile` provides matching preferences. Tempo, valence, and danceability are promising, but using them before the user can express those preferences would be an assumption rather than personalization. Artist should support diversity instead of dominating similarity, while ID and title should remain metadata only.
