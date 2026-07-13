# Content-Based Recommender Design

## Executive Summary

This project uses content-based filtering to rank songs by how closely their attributes match a user's stated preferences. The catalog contains 60 songs and 13 fields. Ten fields can influence recommendation quality; `id`, `title`, and `artist` support identity, display, explanations, and diversity.

The design prioritizes clear user intent while still using the expanded dataset:

- Genre and mood define the listener's high-level goal when selected.
- Six audio features refine how the music should sound and feel.
- Release year and duration provide lightweight contextual refinement.
- Optional preferences are excluded from scoring rather than treated as zero.
- Every recommendation should include a score breakdown that a user can understand.

## Dataset

The catalog is stored in `data/songs.csv`.

| Category | Fields | Purpose |
|---|---|---|
| Identity and display | `id`, `title`, `artist` | Identify songs, display results, and support artist diversity |
| Categorical content | `genre`, `mood` | Represent high-level musical style and listening intent |
| Audio content | `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`, `instrumentalness` | Describe measurable aspects of how a song sounds |
| Context | `release_year`, `duration_seconds` | Represent era and track length |

### Data provenance

The starter dataset supplied the first 10 songs and these fields:

`id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

This project added 50 synthetic songs and three fields:

- `release_year` for era preferences
- `duration_seconds` for track-length preferences
- `instrumentalness` for vocal-versus-instrumental preferences

The added values are synthetic classroom data inspired by common music-catalog and audio-analysis structures. They are not official measurements from Spotify, YouTube, artists, or recording labels.

### Coverage

The catalog contains 57 genre labels and 33 mood labels. It is broad but shallow: lofi appears three times, pop appears twice, and the other 55 genres appear once each. This supports varied demonstrations but limits exact-match choice within most genres.

Numeric coverage is sufficient for testing contrasting profiles:

| Feature | Range |
|---|---:|
| Energy | 0.08-0.98 |
| Tempo | 48-190 BPM |
| Valence | 0.27-0.96 |
| Danceability | 0.08-0.97 |
| Acousticness | 0.01-0.99 |
| Instrumentalness | 0.01-1.00 |
| Release year | 2010-2024 |
| Duration | 154-603 seconds |

## UserProfile Design

The application should use progressive disclosure. Genre and mood remain visible as multi-select controls with an **Any** option. Detailed numeric targets belong under an optional **Advanced preferences** section so a new user is not forced to configure ten controls.

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
| `preferred_release_year` | 2010-2024 slider | `release_year` | Optional |
| `preferred_duration_seconds` | 154-603 second slider | `duration_seconds` | Optional |

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

For example, a user who selects both `rock` and `metal` receives the better of the two comparisons for each song. Selecting **Any** removes the category from scoring rather than awarding every song a perfect match.

Features already stored on a 0-1 scale use absolute distance:

```text
numeric_similarity = 1 - abs(preference - song_value)
```

Tempo, year, and duration use the observed catalog range so their larger units cannot dominate:

```text
tempo_similarity = max(0, 1 - abs(target_tempo - song_tempo) / 142)
year_similarity = max(0, 1 - abs(target_year - song_year) / 14)
duration_similarity = max(0, 1 - abs(target_duration - song_duration) / 449)
```

All text values should be trimmed and converted to lowercase before categorical comparison.

## Category Relationship Maps

Exact-only matching is too brittle for a catalog with 57 genre labels. The first implementation should use explicit, reviewable category families. Two different labels in the same family receive 0.5 similarity.

### Genre families

| Family | Related labels |
|---|---|
| Pop | pop, indie pop, electropop, folk pop, K-pop, J-pop |
| Rock | rock, southern rock, alternative, grunge, post-punk, punk, metal |
| Electronic | EDM, house, techno, trance, dubstep, drum and bass, synthwave, darkwave, downtempo, chiptune |
| Hip-hop and R&B | hip hop, trap, R&B |
| Jazz and soul | jazz, bebop, blues, soul, funk, gospel |
| Folk and country | folk, americana, country, bluegrass, Scandinavian folk |
| Latin and global | Latin, salsa, samba, bossa nova, flamenco, reggaeton, Afrobeat, world, reggae |
| Classical and atmospheric | classical, orchestral, opera, choral, cinematic, ambient, new age, meditation |

### Mood families

| Family | Related labels |
|---|---|
| Positive | happy, hopeful, uplifting, celebratory, playful, euphoric, triumphant |
| Calm | chill, relaxed, peaceful, serene, focused, contemplative, dreamy |
| Intense | intense, energetic, aggressive, angry, rebellious, confident, passionate |
| Dark and reflective | moody, melancholic, dark, mysterious, dramatic, nostalgic |
| Expressive | soulful, spiritual, romantic |
| Exploratory | adventurous, whimsical |

These families are application rules, not universal facts about music. They should be stored as named constants, tested, and revised when the catalog changes. A genre may belong to more than one family in a later version, but one family per label keeps the initial implementation simple.

## Weighted Score

When every preference is active, the weights total 100%.

| Feature | Weight | Design role |
|---|---:|---|
| Genre | 20% | Primary style preference |
| Mood | 20% | Primary listening intent |
| Energy | 12% | Broad activity and intensity signal |
| Tempo | 8% | Pace refinement |
| Valence | 8% | Emotional-tone refinement |
| Danceability | 8% | Movement and activity refinement |
| Acousticness | 8% | Production-style refinement |
| Instrumentalness | 6% | Vocal-versus-instrumental refinement |
| Release year | 5% | Era preference and tie-breaker |
| Duration | 5% | Listening-context preference and tie-breaker |

Only active preferences contribute:

```text
active_weight = sum(weight for each selected preference)

final_score =
    sum(weight * similarity for each selected preference)
    / active_weight
```

Renormalization keeps the result between 0 and 1 and makes partial profiles comparable with complete profiles.

### Why these weights make sense

- Genre and mood receive 40% together because they communicate the user's clearest intent.
- Audio features receive 50% together, adding detail without letting one correlated measurement dominate.
- Year and duration receive 10% together because they should refine recommendations, not override musical compatibility.
- Energy receives the largest numeric weight because it is meaningful across studying, relaxing, exercising, and social listening.

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

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Shallow genre coverage | Most genres have only one exact match | Add more songs per genre and support related-genre partial matches |
| Correlated features | Mood/valence or energy/tempo may be counted twice | Keep individual weights modest and inspect score breakdowns |
| Overspecialization | Results may become too similar | Rerank the final list for genre and artist diversity |
| Missing preferences | Unanswered controls could be treated as minimum values | Store missing values as `None` and renormalize active weights |
| Synthetic data | Results may appear more realistic than the evidence supports | Label the dataset clearly and avoid claims about real user behavior |
| Category-family assumptions | Relatedness rules may oversimplify genre and mood | Keep mappings explicit, test them, and document changes |

## Evaluation Plan

Before adjusting weights, test whether changing one preference moves suitable songs upward while unrelated rankings remain reasonably stable.

Recommended profiles include:

1. Happy high-energy pop with low instrumentalness.
2. Chill low-energy lofi with high instrumentalness.
3. Energetic dance music with high tempo and danceability.
4. Acoustic peaceful music with a longer preferred duration.
5. A partial profile containing only multiple genres and moods to verify best-match scoring and weight renormalization.
6. An **Any genre** profile to verify that genre is excluded instead of treated as a perfect match.

For each profile, record the top results, score breakdowns, unexpected rankings, and whether the explanation matches the actual calculation.

## Implementation Sequence

1. Expand `UserProfile` with the optional fields above and validate that at least one is active.
2. Parse and validate all 13 CSV columns.
3. Normalize categorical text and implement the genre and mood family maps.
4. Implement exact, related, and numeric similarity functions independently.
5. Implement best-match scoring for multi-select categories.
6. Implement weighted scoring with active-weight renormalization.
7. Return score breakdowns for explanations and debugging.
8. Add ranking, diversity handling, and tests for full, partial, multi-select, and **Any** profiles.

## Decision Summary

The final design uses all meaningful content features while keeping the user experience manageable. Multi-select genre and mood preferences establish intent without requiring one exact label. Explicit category families give related songs partial credit. Audio attributes refine musical character, while year and duration provide contextual tie-breaking. Optional controls, normalized similarities, and active-weight renormalization make the design explainable, testable, and appropriate for the current 60-song simulator.
