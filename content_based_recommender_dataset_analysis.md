# Content-Based Recommender Design

## Executive Summary

This project uses content-based filtering to rank songs by how closely their attributes match a user's stated preferences. The catalog contains 60 songs and 15 fields. Twelve fields can influence recommendation quality; `id`, `title`, and `artist` support identity, display, explanations, and diversity.

The design prioritizes clear user intent while still using the expanded dataset:

- Genre and mood define the listener's high-level goal when selected.
- Seven audio features refine how the music should sound, feel, and whether it resembles a live recording.
- Release year, duration, and popularity provide lightweight contextual refinement.
- Optional preferences are excluded from scoring rather than treated as zero.
- Every recommendation should include a score breakdown that a user can understand.

## Dataset

The catalog is stored in `data/songs.csv`.

| Category | Fields | Purpose |
|---|---|---|
| Identity and display | `id`, `title`, `artist` | Identify songs, display results, and support artist diversity |
| Categorical content | `genre`, `mood` | Represent high-level musical style and listening intent |
| Audio content | `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`, `instrumentalness`, `liveness` | Describe aspects of how a song sounds and its recording environment |
| Context | `release_year`, `duration_seconds`, `popularity` | Represent era, track length, and a simulated mainstream-versus-discovery signal |

### Data provenance

The starter dataset supplied the first 10 songs and these fields:

`id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

This project added 50 synthetic songs and five fields:

- `release_year` for era preferences and derived decade groupings
- `duration_seconds` for track-length preferences
- `instrumentalness` for vocal-versus-instrumental preferences
- `popularity` for optional mainstream-versus-discovery preferences
- `liveness` for optional studio-versus-live-performance preferences

The added values are synthetic classroom data inspired by common music-catalog and audio-analysis structures. They are not official measurements from Spotify, YouTube, artists, or recording labels. Popularity does not represent real stream counts or chart performance, and liveness was not produced by an audio-analysis model. During dataset consolidation, only the genre and mood labels in rows 11-60 were normalized. Adding popularity and liveness appended new values without changing the 13 fields already stored for any song, including the original 10 starter rows.

Release decade is derived from `release_year` rather than stored or scored separately. This avoids counting the same era preference twice while retaining the more precise year value.

### Coverage

The catalog now contains 13 genres and 9 moods. Every genre has 3-7 songs, and every mood has 3-9 songs. This provides enough overlap to compare several candidates for the same preference while retaining meaningful variety.

| Genre | Songs | Genre | Songs |
|---|---:|---|---:|
| ambient | 4 | jazz | 6 |
| classical | 5 | latin | 6 |
| electronic | 7 | lofi | 3 |
| folk | 5 | pop | 4 |
| hip hop | 4 | rock | 7 |
| indie pop | 3 | synthwave | 3 |
| world | 3 |  |  |

| Mood | Songs | Mood | Songs |
|---|---:|---|---:|
| celebratory | 8 | intense | 9 |
| chill | 8 | moody | 9 |
| confident | 5 | relaxed | 6 |
| focused | 3 | romantic | 6 |
| happy | 6 |  |  |

Numeric coverage is sufficient for testing contrasting profiles:

| Feature | Range |
|---|---:|
| Energy | 0.08-0.98 |
| Tempo | 48-190 BPM |
| Valence | 0.27-0.96 |
| Danceability | 0.08-0.97 |
| Acousticness | 0.01-0.99 |
| Instrumentalness | 0.01-1.00 |
| Liveness | 0.04-0.83 |
| Popularity | 29-90 |
| Release year | 2010-2024 |
| Duration | 154-603 seconds |

## UserProfile Design

The application should use progressive disclosure. Genre and mood remain visible as multi-select controls with an **Any** option. Detailed numeric targets belong under an optional **Advanced preferences** section so a new user is not forced to configure twelve controls.

| UserProfile field | UI control | Compared with | Status |
|---|---|---|---|
| `preferred_genres` | Multi-select plus Any | `genre` | Optional |
| `preferred_moods` | Multi-select plus Any | `mood` | Optional |
| `target_energy` | 0-1 slider | `energy` | Optional |
| `target_tempo_bpm` | 48-190 BPM slider | `tempo_bpm` | Optional |
| `target_valence` | 0-1 "positivity" slider | `valence` | Optional |
| `target_danceability` | 0-1 slider | `danceability` | Optional |
| `target_acousticness` | 0-1 slider | `acousticness` | Optional |
| `target_instrumentalness` | 0-1 slider | `instrumentalness` | Optional |
| `target_liveness` | 0-1 studio-to-live slider | `liveness` | Optional |
| `preferred_release_year` | 2010-2024 slider | `release_year` | Optional |
| `preferred_duration_seconds` | 154-603 second slider | `duration_seconds` | Optional |
| `target_popularity` | 0-100 discovery-to-mainstream slider | `popularity` | Optional |

`target_acousticness` replaces the earlier `likes_acoustic` Boolean. A continuous value can represent electronic, mixed, neutral, and strongly acoustic preferences instead of forcing a yes-or-no choice.

An empty multi-select, **Any**, or a numeric value of `None` means **no preference**. It must be excluded from the score. It must not be converted to zero, because zero is a valid target for several audio features.

The profile is valid when at least one preference is active. If every field is empty, the app should ask the user to select a preference instead of returning an arbitrary ranking.

## Similarity Calculations

Every feature produces a similarity from 0 to 1, where 1 is the closest possible match.

Categorical features use the best match across the user's selections:

```text
exact match = 1.0
related category = 0.5
unrelated category = 0.0

category_similarity = max(
    similarity(song_value, selected_value)
    for selected_value in user_selections
)
```

For example, a user who selects both `pop` and `indie pop` receives the better of the two comparisons for each song. Selecting **Any** removes the category from scoring rather than awarding every song a perfect match.

Features already stored on a 0-1 scale use absolute distance:

```text
numeric_similarity = 1 - abs(preference - song_value)
```

Tempo, year, duration, and popularity use a normalizing range so their larger units cannot dominate:

```text
tempo_similarity = max(0, 1 - abs(target_tempo - song_tempo) / 142)
year_similarity = max(0, 1 - abs(target_year - song_year) / 14)
duration_similarity = max(0, 1 - abs(target_duration - song_duration) / 449)
popularity_similarity = max(0, 1 - abs(target_popularity - song_popularity) / 100)
```

All text values should be trimmed and converted to lowercase before categorical comparison.

## Developer-Defined Category Relationships

Dataset consolidation makes exact matching practical, so the system does not require broad genre and mood families. A small set of developer-defined relationships may receive 0.5 similarity as an optional discovery heuristic. These relationships are design assumptions rather than objective facts or patterns learned by AI.

### Related genre pairs

| Genre | Related genre |
|---|---|
| pop | indie pop |
| lofi | ambient |
| electronic | synthwave |
| latin | world |

### Related mood pairs

| Mood | Related mood |
|---|---|
| happy | celebratory |
| chill | relaxed |
| chill | focused |
| intense | confident |

These pairs are application rules, not universal facts about music. A fixed value of 0.5 also assumes that every listed pair is equally related in every listening context. In practice, musical similarity can vary by individual song, listener, culture, activity, and time. The pairs should therefore be stored as named constants, documented, tested independently, and easy to disable. Labels not listed as a pair receive no partial category credit.

### Preferred alternative for this simulator

The recommended baseline is exact genre and mood matching combined with numeric audio-feature similarity. Energy, tempo, valence, danceability, acousticness, instrumentalness, and liveness can identify compatible songs across category boundaries without declaring their genres or moods related. Related-category credit can then be evaluated as an optional experiment rather than treated as required logic.

A data-rich production system could learn category or song relationships from representative playlist co-occurrence and user behavior such as plays, skips, likes, and replays. This simulator does not contain that behavioral evidence, so it should not present its relationships as learned recommendations.

## Weighted Score

When every preference is active, the weights total 100%.

| Feature | Weight | Design role |
|---|---:|---|
| Genre | 18% | Primary style preference |
| Mood | 18% | Primary listening intent |
| Energy | 11% | Broad activity and intensity signal |
| Tempo | 7% | Pace refinement |
| Valence | 7% | Emotional-tone refinement |
| Danceability | 7% | Movement and activity refinement |
| Acousticness | 7% | Production-style refinement |
| Instrumentalness | 6% | Vocal-versus-instrumental refinement |
| Liveness | 5% | Studio-versus-live recording refinement |
| Release year | 5% | Era preference and tie-breaker |
| Duration | 4% | Listening-context preference and tie-breaker |
| Popularity | 5% | Mainstream-versus-discovery refinement |

Only active preferences contribute:

```text
active_weight = sum(weight for each selected preference)

final_score =
    sum(weight * similarity for each selected preference)
    / active_weight
```

Renormalization keeps the result between 0 and 1 and makes partial profiles comparable with complete profiles.

### Why these weights make sense

- Genre and mood receive 36% together because they communicate the user's clearest intent without overwhelming cross-category audio similarity.
- Audio features receive 50% together, adding detail without letting one correlated measurement dominate.
- Year, duration, and popularity receive 14% together because contextual signals should refine recommendations, not override musical compatibility.
- Energy receives the largest numeric weight because it is meaningful across studying, relaxing, exercising, and social listening.
- Popularity receives only 5% because exposure is not the same as quality or personal relevance.

These are transparent starting assumptions, not learned weights. Evaluation should determine whether they behave as intended.

## Recommendation Flow

```text
UserProfile + Song catalog
    -> validate and normalize values
    -> calculate similarities for active preferences
    -> apply weights and renormalize
    -> sort songs by descending score
    -> optionally rerank for artist diversity
    -> return top k songs with explanations
```

An explanation should identify the strongest real matches and avoid claiming that every active feature matched. For example:

> Recommended because it matches your pop and happy preferences, its 0.82 energy is close to your 0.80 target, and its 211-second duration is near your preferred 210 seconds.

## Expected Biases and Risks

The recommender is deterministic, but its results are not neutral. They reflect the catalog, consolidated labels, limited category relationships, and weights selected by the developer.

| Bias or risk | Expected impact | Mitigation |
|---|---|---|
| Genre and mood weighting | Their combined 36% may hide songs with excellent audio-feature matches but different labels | Compare rankings with reduced category weights and show score breakdowns |
| Representation bias | Genre counts range from 3-7 and mood counts from 3-9, so some preferences still have more candidates | Evaluate results by category and add examples to smaller groups when needed |
| Correlated features | Mood/valence or energy/tempo may be counted twice | Keep individual weights modest and inspect score breakdowns |
| Overspecialization | Results may become too similar | Rerank the final list for genre and artist diversity |
| Missing preferences | Unanswered controls could be treated as minimum values | Store missing values as `None` and renormalize active weights |
| Synthetic-data bias | Hand-assigned audio values may reinforce expected stereotypes, such as assuming all lofi is calm | Label the data clearly and test for unexpected feature/category patterns |
| Popularity feedback loop | Favoring already popular songs can reduce discovery and repeatedly expose the same items | Keep popularity optional and low-weighted; compare results with the feature disabled |
| Synthetic liveness | Hand-assigned values may confuse energetic studio tracks with genuinely live recordings | Treat liveness as an estimate, inspect edge cases, and avoid claims of measured audio confidence |
| Related-category assumptions | Hand-written pairs and a fixed 0.5 similarity may oversimplify relationships that vary by listener and context | Use exact category plus numeric similarity as the baseline; keep related pairs explicit, optional, tested, documented, and easy to disable |

## Evaluation Plan

Before adjusting weights, test whether changing one preference moves suitable songs upward while unrelated rankings remain reasonably stable.

Recommended profiles include:

1. Happy high-energy pop with low instrumentalness.
2. Chill low-energy lofi with high instrumentalness.
3. Energetic dance music with high tempo and danceability.
4. Acoustic peaceful music with a longer preferred duration.
5. A partial profile containing only multiple genres and moods to verify best-match scoring and weight renormalization.
6. An **Any genre** profile to verify that genre is excluded instead of treated as a perfect match.
7. A high-popularity, high-liveness profile to verify that contextual preferences refine rather than dominate musical compatibility.
8. A low-popularity studio profile to verify that discovery-oriented preferences can surface niche candidates.

For each profile, record the top results, score breakdowns, unexpected rankings, and whether the explanation matches the actual calculation.

## Implementation Sequence

1. Expand `UserProfile` with the optional fields above and validate that at least one is active.
2. Parse and validate all 15 CSV columns.
3. Normalize categorical text and implement the genre and mood family maps.
4. Implement exact, related, and numeric similarity functions independently.
5. Implement best-match scoring for multi-select categories.
6. Implement weighted scoring with active-weight renormalization.
7. Return score breakdowns for explanations and debugging.
8. Add ranking, diversity handling, and tests for full, partial, multi-select, and **Any** profiles.

## Decision Summary

The final design uses all meaningful content features while keeping the user experience manageable. The consolidated 13-genre and 9-mood vocabulary provides several exact-match candidates per category. Multi-select preferences establish intent, while a limited set of optional related-category pairs supports discovery. Audio attributes, including liveness, refine musical character and recording context; year, duration, and popularity provide low-weight contextual tie-breaking. Optional controls, normalized similarities, and active-weight renormalization make the design explainable and testable for the current 60-song simulator.
