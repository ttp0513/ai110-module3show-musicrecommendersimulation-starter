# Scoring Sensitivity Experiment

## Purpose

This small experiment measures how recommendation rankings respond to two isolated logic changes:

1. **Weight shift:** Double the energy weight and halve the genre weight.
2. **Feature removal:** Exclude mood from scoring.

The experiment is limited to score behavior, ranking changes, and mathematical validation.

## Method

All experiments used the same 60-song catalog and the six profiles defined in `src/main.py`. Each run returned the top five songs.

| Profile | Active preferences |
|---|---|
| High-Energy Pop | Pop, Happy, energy 0.90, valence 0.85, danceability 0.85 |
| Chill Lofi | Lofi, Chill, energy 0.20, acousticness 0.70, instrumentalness 0.85 |
| Deep Intense Rock | Rock, Intense, energy 0.90, valence 0.25, tempo 150 BPM |
| Sad but Euphoric | Sad, energy 0.95, valence 0.95 |
| Moody but Euphoric | Moody, energy 0.95, valence 0.95 |
| Popularity Only | Popularity 100 |

The sensitivity variants were run in memory. The stored feature weights and scoring code were restored after each run.

## Baseline Formula

For active preferences, the recommender calculates:

```text
final score =
sum(feature similarity x feature weight)
------------------------------------------------
sum(weights belonging to active preferences)
```

The denominator renormalizes the active weights. Therefore, an unselected or removed feature contributes neither score nor weight.

## Experiment 1: Weight Shift

The temporary changes were:

```python
FEATURE_WEIGHTS["energy"] = 0.22  # baseline: 0.11
FEATURE_WEIGHTS["genre"] = 0.09   # baseline: 0.18
```

The raw weight total changed from `1.00` to `1.02`. This does not invalidate the final score because active-weight renormalization still makes the normalized active weights sum to `1.0`. If a configuration file must visibly total 100%, every shifted weight can be divided by `1.02`; applying that common scale would not change the rankings.

| Profile | Baseline first result | Weight-shift first result | Main ranking effect |
|---|---|---|---|
| High-Energy Pop | Sunrise City, 97.8 | Sunrise City, 96.4 | First place stayed stable; Lagos Sunrise entered the top five and the middle order changed |
| Chill Lofi | Midnight Coding, 95.6 | Library Rain, 92.3 | Library Rain moved to first and Temple Bells entered the top five |
| Deep Intense Rock | Concrete Weather, 98.8 | Concrete Weather, 98.8 | The same five songs remained in the same order |
| Sad but Euphoric | Neon Festival, 48.5 | Neon Festival, 60.3 | The same first result remained, while the stronger energy weight raised scores and changed lower positions |
| Moody but Euphoric | Machine Pulse, 86.4 | Machine Pulse, 87.9 | The top-five order stayed stable with modest score changes |
| Popularity Only | Starlight Signal, 90.0 | Starlight Signal, 90.0 | No change because genre and energy were inactive |

## Experiment 2: Mood Removal

Mood removal was simulated by omitting `preferred_moods` from each profile. This follows the normal `score_song()` path: when mood is absent, the mood similarity tuple is never added. It is mathematically equivalent to temporarily disabling the mood-scoring block, without editing the source file.

Mood was removed from both the weighted numerator and the active-weight denominator. Leaving the mood weight in the denominator with a zero similarity would incorrectly penalize every song.

| Profile | Baseline first result | First result without mood | Main ranking effect |
|---|---|---|---|
| High-Energy Pop | Sunrise City, 97.8 | Gym Hero, 97.4 | Gym Hero moved from fifth to first; Paper Moon Parade entered the top five |
| Chill Lofi | Midnight Coding, 95.6 | Midnight Coding, 93.6 | First place stayed stable, but Focus Flow rose and Deep Current entered the top five |
| Deep Intense Rock | Concrete Weather, 98.8 | Concrete Weather, 98.3 | The same five songs remained in the same order with lower scores |
| Sad but Euphoric | Neon Festival, 48.5 | Neon Festival, 97.1 | The same first result remained, but removing the unmatched mood nearly doubled the score |
| Moody but Euphoric | Machine Pulse, 86.4 | Neon Festival, 97.1 | The complete top five changed to high-energy, high-valence songs |
| Popularity Only | Starlight Signal, 90.0 | Starlight Signal, 90.0 | No change because mood was already inactive |

## Math Verification

Every variant was evaluated across all 60 songs for all six profiles.

| Configuration | Minimum observed score | Maximum observed score | All scores within 0-1 | Normalized active weights sum to 1 |
|---|---:|---:|---|---|
| Baseline | 0.140161 | 0.988435 | Yes | Yes |
| Energy doubled; genre halved | 0.140161 | 0.988435 | Yes | Yes |
| Mood removed | 0.146667 | 0.983056 | Yes | Yes |

The results confirm that both experiments preserve the scoring formula and valid score bounds. They also demonstrate that ranking sensitivity depends on which features are active: changing an inactive feature has no effect, while removing a high-weight active feature can substantially reorder results.
