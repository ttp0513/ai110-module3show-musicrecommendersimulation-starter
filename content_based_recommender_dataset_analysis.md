# Content-Based Recommender Dataset Analysis

## Purpose

This document examines `data/songs.csv` from a system-design perspective and identifies which attributes are effective for a simple content-based music recommender. The analysis is specific to the current simulator, its expanded 60-song catalog, and the existing `Song` and `UserProfile` classes.

## Dataset Overview

The dataset contains **60 songs and 13 attributes**. Rows 1-10 are the starter catalog. Rows 11-60 are synthetic educational records designed to resemble the ranges and combinations found in real audio-feature datasets; their values must not be described as measurements supplied by Spotify or YouTube.

### Feature provenance

The starter CSV supplied `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. This project later added `release_year`, `duration_seconds`, and `instrumentalness` to support deeper content analysis. These additions reflect categories commonly found in music-catalog or audio-analysis data:

- `release_year` represents catalog metadata and supports era analysis.
- `duration_seconds` represents track-length metadata in a human-readable unit.
- `instrumentalness` is a synthetic 0-1 audio descriptor for comparing vocal-heavy and instrumental tracks.

All values in the added columns are synthetic classroom data. They are plausible for testing the simulator but are not official values from Spotify, YouTube, an artist, or a recording label.

| Attribute | Type | Observed values or range | Recommended role |
|---|---|---|---|
| `id` | Integer identifier | 1-60 | Identity only; do not score |
| `title` | Text metadata | Unique song titles | Display and explanation only |
| `artist` | Categorical metadata | 58 artists | Optional preference/diversity signal |
| `genre` | Categorical feature | 57 labels | Strong scoring feature |
| `mood` | Categorical feature | 33 labels | Strong scoring feature |
| `energy` | Numeric feature | 0.08-0.98 | Strong scoring feature |
| `tempo_bpm` | Numeric feature | 48-190 BPM | Useful optional feature |
| `valence` | Numeric feature | 0.27-0.96 | Useful optional feature |
| `danceability` | Numeric feature | 0.08-0.97 | Useful optional feature |
| `acousticness` | Numeric feature | 0.01-0.99 | Strong scoring feature |
| `release_year` | Integer metadata | 2010-2024 | Useful optional era feature |
| `duration_seconds` | Integer feature | 154-603 seconds | Useful optional length feature |
| `instrumentalness` | Numeric feature | 0.01-1.00 | Useful optional vocal/instrumental feature |

Numeric averages in this catalog are:

- Energy: **0.671**
- Tempo: **110.7 BPM**
- Valence: **0.674**
- Danceability: **0.654**
- Acousticness: **0.444**
- Release year: **2019**
- Duration: **265 seconds** (about **4 minutes 25 seconds**)
- Instrumentalness: **0.376**

## Dataset Coverage

### Genre distribution

| Genre | Songs |
|---|---:|
| lofi | 3 |
| pop | 2 |
| 55 other genres | 1 each |

### Mood distribution

| Mood | Songs |
|---|---:|
| celebratory | 3 |
| chill | 3 |
| confident | 3 |
| peaceful | 3 |
| 16 moods | 2 each |
| 13 moods | 1 each |

The expanded catalog has much broader cultural and stylistic coverage, including hip hop, R&B, classical, country, folk, reggae, metal, punk, house, techno, trance, soul, funk, blues, Latin styles, Afrobeat, gospel, orchestral, disco, drum and bass, K-pop, J-pop, opera, choral, and other genres. However, breadth is not the same as depth: 55 of the 57 genre labels occur only once. Exact genre matching will therefore find few alternatives for most profiles. A production catalog would need many songs per genre as well as careful handling of subgenres and multi-genre songs.

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

Energy is numeric and has good separation across the catalog, from 0.08 to 0.98. It supports more precise matching than a category because the system can reward closeness rather than require equality.

A simple similarity calculation is:

```text
energy_similarity = 1 - abs(user_target_energy - song_energy)
```

Because both values use a 0-1 scale, the result is also between 0 and 1. A song at 0.82 energy is therefore a closer match to a target of 0.80 than a song at 0.40.

**Recommendation:** Use in V1 as a continuous similarity score.

### 4. Acousticness: effective with careful profile mapping

Acousticness has a wide range, from 0.01 to 0.99, so it clearly distinguishes electronic or heavily produced tracks from acoustic tracks. The current `UserProfile` represents the preference as the Boolean `likes_acoustic`, while songs use a continuous 0-1 value.

For a simple implementation, map `likes_acoustic=True` to a high target such as 0.8 and `False` to a low target such as 0.2, then score numeric closeness. This is more informative than using an arbitrary hard cutoff.

The Boolean profile is still restrictive: a user who does not specifically prefer acoustic music may not actively dislike it. A later version should replace it with `target_acousticness: float` or make this preference optional.

**Recommendation:** Use in V1, but give it less weight than genre, mood, and energy.

### 5. Tempo: useful after expanding the user profile

Tempo ranges from 48 to 190 BPM and can distinguish slow meditation or ambient music from faster dance, punk, or jazz tracks. However, the existing `UserProfile` has no target tempo, so the recommender currently has nothing meaningful to compare it with. Inferring a user's desired tempo from energy would duplicate information and could make the score appear more confident without adding a real preference.

If `target_tempo_bpm` is added later, similarity can be based on normalized distance. The normalization must prevent tempo from dominating merely because it uses a much larger numeric scale than the 0-1 features.

**Recommendation:** Exclude from V1 scoring; add when the profile accepts a tempo preference.

### 6. Valence: useful after expanding the user profile

Valence estimates musical positivity. The expanded range of 0.27-0.96 can distinguish brighter from darker-sounding tracks, but the current profile does not store a valence target. It may also overlap conceptually with labels such as `happy`, `celebratory`, `melancholic`, and `dark`.

**Recommendation:** Exclude from V1. Consider it later as a continuous alternative or supplement to mood, while avoiding double-counting the same concept.

### 7. Danceability: useful after expanding the user profile

Danceability ranges from 0.08 to 0.97 and could improve party, exercise, or movement-focused recommendations. It is not represented in the current user profile.

**Recommendation:** Exclude from V1. Add an optional danceability preference in an expanded simulator.

### 8. Release year: useful for era preferences

Release year supports preferences such as newer releases, 2010s music, or older catalog tracks. Its observed range is 2010-2024. Year should not be mixed directly with 0-1 features because its scale is much larger. A target-year similarity can divide the year difference by the catalog's 14-year span and clamp the result to 0-1.

**Recommendation:** Keep for analysis now; score it only after adding a preferred year or era to `UserProfile`.

### 9. Duration: useful for listening context

`duration_seconds` ranges from 154 to 603 seconds, or approximately 2 minutes 34 seconds to 10 minutes 3 seconds. Seconds are easier to read in this classroom dataset and provide enough precision for recommendation analysis. Duration can distinguish quick playlist tracks from long ambient, meditation, orchestral, or performance pieces. It may be useful when the user has limited time or wants extended focus music.

**Recommendation:** Keep for analysis now; score normalized duration distance only when a user supplies a preferred length or range.

### 10. Instrumentalness: effective for vocal preference

Instrumentalness ranges from 0.01 to 1.00 and adds information that acousticness does not provide. A song can be electronic and instrumental, or acoustic and vocal. This makes instrumentalness especially useful for study, meditation, soundtrack, classical, and spoken-word distinctions.

**Recommendation:** Add `target_instrumentalness` to a future `UserProfile`, then use `1 - abs(target_instrumentalness - song.instrumentalness)`.

### 11. Artist: limited as a scoring feature

Artist is useful metadata, but only Neon Echo and LoRoom appear more than once. Exact artist matching would still be unreliable and could over-recommend familiar artists. Artist is more useful for controlling diversity, such as preventing the top results from being dominated by one artist.

**Recommendation:** Do not include in the core V1 score. Use for tie-breaking, explanations, or a one-song-per-artist diversity rule.

### 12. ID and title: not recommendation features

`id` identifies a record, and `title` presents it to the user. Neither describes musical similarity. Scoring them would introduce arbitrary behavior.

**Recommendation:** Use only for identity, display, logging, and explanations.

## Suggested Features for a Deeper Dataset

Large music and video platforms do not rely on one handcrafted score. They can combine audio analysis, catalog metadata, search and session context, and behavioral signals such as plays, repeats, skips, likes, saves, and watch time. The simulator can borrow the structure of common audio-feature datasets without claiming to reproduce a platform's private recommendation system.

Release year, duration, and instrumentalness are now active dataset columns. The following additional numerical columns could add more content information in a future CSV version:

| Proposed feature | Typical representation | Recommender value |
|---|---|---|
| `speechiness` | 0-1 | Helps distinguish spoken word and rap-heavy tracks from mostly sung or instrumental music |
| `liveness` | 0-1 | Indicates whether a recording sounds like a live performance |
| `loudness_db` | Negative decibels, commonly closer to 0 for louder tracks | Adds production intensity that energy alone may not capture |
| `instrumental_complexity` | Project-defined 0-1 score | Can separate minimal background music from dense arrangements |
| `vocal_presence` | Project-defined 0-1 score | Provides an intuitive alternative to treating instrumentalness as a strict inverse |

If behavioral simulation is added later, useful numerical signals include `play_count`, `completion_rate`, `skip_rate`, `like_rate`, `save_rate`, and `repeat_count`. These are interaction features rather than properties of the song itself, so using them would move the project toward a hybrid or collaborative recommender. Popularity signals must be capped or normalized carefully; otherwise already-popular songs can crowd out new and niche music.

New fields should be added to the score only when the `UserProfile` or interaction model contains something meaningful to compare against them. Instrumentalness works best with a user field such as `target_instrumentalness`, while `duration_seconds` could pair with `preferred_duration_seconds` and `release_year` with `preferred_era`. All 0-1 features can use absolute-distance similarity. Loudness, duration, tempo, and year need their own normalization rules because their units and ranges differ.

## Simple Scoring Design

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

Sixty songs are enough to exercise ranking and filtering behavior, but they are still too few for reliable personalization. The catalog now has broad genre coverage but usually only one song per genre, so results may contain weak categorical matches simply because there are no same-genre alternatives.

**Mitigation:** Show match scores and explanations, and avoid presenting the results as predictions of what the user will definitely like.

### Representation imbalance

Lofi/chill profiles have more exact-match options than profiles for the many genres represented once. This can create an experience-quality difference between users.

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

## Development Path

1. Implement the four-feature V1 score using genre, mood, energy, and acousticness.
2. Return a score breakdown so each recommendation can be inspected and explained.
3. Test contrasting profiles, including happy pop, chill lofi, intense rock, and acoustic jazz.
4. Check whether each profile has enough suitable candidates and document catalog gaps.
5. Add optional tempo, valence, danceability, instrumentalness, duration, or era preferences one at a time and compare the rankings before keeping them.
6. Add multiple songs per genre before attempting complex similarity models or learning weights from behavior.

## Conclusion

For the current simulator, **genre, mood, energy, and acousticness** form the most effective simple content-based scoring set because the existing `UserProfile` provides matching preferences. Tempo, valence, danceability, instrumentalness, duration, and release year deepen the dataset and support future experiments, but scoring them before the user can express those preferences would be an assumption rather than personalization. Artist should support diversity instead of dominating similarity, while ID and title should remain metadata only.
