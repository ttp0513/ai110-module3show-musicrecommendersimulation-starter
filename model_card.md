# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

This name reflects the goal of matching songs to a listener's preferred sound and mood.

---

## 2. Intended Use

VibeMatch generates ranked song recommendations. It is a CLI-first classroom simulation.

The system is designed for students learning about recommender systems. It is not a production music service. It does not predict whether a real person will like a song.

The system assumes that the user can describe their current preferences. The user can select categories such as genre and mood. The user can also provide numeric targets such as energy or danceability.

The output includes five songs, compatibility scores, and reasons. The scores show similarity to the selected preferences. They are not probabilities.

---

## 3. How the Model Works

VibeMatch uses content-based filtering. It compares one user profile with every song in the catalog.

The model can consider these song features:

- Genre and mood.
- Energy and tempo.
- Valence and danceability.
- Acousticness and instrumentalness.
- Liveness.
- Release year and duration.
- Popularity.

An exact genre or mood match receives full similarity. A small set of related categories receives partial similarity. Unrelated categories receive zero similarity.

Numeric features use distance. A song closer to the user's target receives a higher similarity. A song farther away receives a lower similarity.

Each active feature has a weight. The system multiplies similarity by weight. It then adds the results. Unselected preferences are excluded. The remaining active weights are normalized before the final score is returned.

The starter logic used fewer preferences and simpler scoring.

---

## 4. Data

The catalog contains 60 songs. The starter catalog contained 10 songs. The project added 50 synthetic songs without changing the original rows.

The catalog contains 13 genres:

- Ambient, classical, electronic, folk, and hip hop.
- Indie pop, jazz, Latin, lofi, and pop.
- Rock, synthwave, and world.

The catalog contains nine moods:

- Celebratory, chill, confident, focused, and happy.
- Intense, moody, relaxed, and romantic.

Each row has 15 fields. Five fields were added during the project: release year, duration, instrumentalness, popularity, and liveness.

The song names and most metadata are synthetic. Popularity and liveness are classroom estimates. They are not measurements from Spotify, YouTube, or audio analysis.

The dataset does not cover every musical culture or listener need. It does not include a `sad` mood. It also lacks lyrics, language, location, and real listening history.

---

## 5. Strengths

The model works well when the catalog contains several songs that match the user's categories.

The High-Energy Pop profile returned Pop and related Indie Pop songs. The Chill Lofi profile returned Lofi songs first. It also found related Ambient songs. The Deep Intense Rock profile returned five Rock and Intense songs.

The scoring system handles partial profiles. It ignores missing preferences instead of treating them as zero. This prevents an unanswered control from becoming a negative preference.

The output is easy to inspect. It shows strong matches, partial matches, and mismatches. It also shows which features were not considered.

The same inputs always produce the same ranking. This makes the model easy to test and debug.

---

## 6. Limitations and Bias

The catalog is small. Some genres and moods have more examples than others. Users with common preferences have more choices.

The category relationships were written by the developer. They are not learned from listener behavior. They may reflect personal or cultural assumptions.

The feature weights are also developer choices. Genre and mood can dominate some profiles. Related numeric features may count a similar idea more than once. Energy, tempo, and danceability are one example.

Unsupported labels are not rejected. The test profile requested `sad`, but `sad` is not in the dataset. The system still returned celebratory songs because their energy and valence were close.

Sparse profiles can be misleading. A popularity-only profile becomes a popularity ranking. It does not represent broad musical taste.

Conflicting preferences can still produce high scores. The Moody but Euphoric profile ranked exact Moody songs even when their valence was far from the target.

The numeric distance formula is simple and linear. The same energy gap receives the same penalty in every context. The model cannot understand that two listeners may interpret energy differently.

The system has no plays, skips, likes, replays, or playlist history. It cannot learn or update a user's taste automatically.

---

## 7. Evaluation

I tested three realistic profiles:

1. High-Energy Pop.
2. Chill Lofi.
3. Deep Intense Rock.

I also tested three difficult profiles:

1. Sad but Euphoric.
2. Moody but Euphoric.
3. Popularity Only.

For each profile, I reviewed the top five songs. I checked the order, score, genre, mood, and explanation. The complete CLI output appears in the README under **Experiments You Tried**.

I also ran two sensitivity experiments. I doubled the energy weight and halved the genre weight. I then removed mood from scoring. These changes showed which rankings were stable and which relied heavily on one feature.

The normalized active weights still summed to 1. All scores stayed between 0 and 1. The full calculations appear in the [Scoring Sensitivity Experiment](scoring_sensitivity_experiment.md).

The most surprising result came from the unsupported `sad` mood. Every song received zero mood credit. The system still returned upbeat songs because it had no validation rule to stop the ranking.

---

## 8. Future Work

I would validate genre and mood before scoring. An unsupported value should show a warning or suggest supported alternatives.

I would add a minimum-input rule. A user should select more than popularity alone before receiving a personalized result.

I would detect conflicting preferences. The interface could explain the conflict before ranking songs.

I would add a diversity step after scoring. This could limit repeated artists, genres, or moods in the top five.

I would use real listening behavior when available. Plays, skips, likes, and replays could support a hybrid recommender.

I would test learned category relationships instead of relying only on hand-written pairs. I would also add lyrics, language, and artist similarity.

---

## 9. Personal Reflection

My biggest learning moment was understanding active-weight normalization. Removing a preference must remove both its score contribution and its weight. Otherwise, the model unfairly lowers every result.

AI tools helped me expand the dataset, review the design, suggest edge cases, and format explanations. They also helped me compare several profiles quickly. I still needed to check the CSV types, feature ranges, formulas, and terminal output. I also checked that the original rows were preserved. AI suggestions about related genres and moods needed extra review because those choices are subjective.

I was surprised that a weighted sum could feel like a real recommendation. A song title, a score, and a few clear reasons made the result feel personal. The sensitivity tests showed that this feeling can be misleading when the input is unsupported or too narrow.

If I extended the project, I would build input validation first. I would then add diversity reranking and listener feedback. Finally, I would compare this content-based model with a collaborative or hybrid recommender.
