from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

# Proposed weights in the recommender system
FEATURE_WEIGHTS = {
    "genre": 0.18,
    "mood": 0.18,
    "energy": 0.11,
    "tempo_bpm": 0.07,
    "valence": 0.07,
    "danceability": 0.07,
    "acousticness": 0.07,
    "instrumentalness": 0.06,
    "liveness": 0.05,
    "release_year": 0.05,
    "duration_seconds": 0.04,
    "popularity": 0.05,
}

# Proposed score_song matching
EXACT_SCORE = 1.0
RELATED_SCORE = 0.5
UNRELATED_SCORE = 0.0

# Developer-defined category relationships. Frozensets make each
# relationship bidirectional, so each pair only needs to be declared once.
RELATED_GENRE_PAIRS = {
    frozenset(("pop", "indie pop")),
    frozenset(("lofi", "ambient")),
    frozenset(("electronic", "synthwave")),
    frozenset(("latin", "world")),
}

RELATED_MOOD_PAIRS = {
    frozenset(("happy", "celebratory")),
    frozenset(("chill", "relaxed")),
    frozenset(("chill", "focused")),
    frozenset(("intense", "confident")),
}

DYNAMIC_RANGE_FEATURES = (
    "tempo_bpm",
    "release_year",
    "duration_seconds",
)

NUMERIC_FEATURE_CONFIG = (
    # song feature, userprofile preference field, fixed range, unit, decimals
    ("energy", "target_energy", 1.0, "", 2),
    (
        "tempo_bpm",
        "target_tempo_bpm",
        None,
        " BPM",
        0,
    ),
    ("valence", "target_valence", 1.0, "", 2),
    (
        "danceability",
        "target_danceability",
        1.0,
        "",
        2,
    ),
    (
        "acousticness",
        "target_acousticness",
        1.0,
        "",
        2,
    ),
    (
        "instrumentalness",
        "target_instrumentalness",
        1.0,
        "",
        2,
    ),
    (
        "liveness",
        "target_liveness",
        1.0,
        "",
        2,
    ),
    (
        "release_year",
        "preferred_release_year",
        None, # Do not use a fixed range; retrieve the current range from feature_ranges.
        "",
        0,
    ),
    (
        "duration_seconds",
        "preferred_duration_seconds",
        None,
        " seconds",
        0,
    ),
    (
        "popularity",
        "target_popularity",
        100.0,
        "/100",
        0,
    ),
)

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    release_year: int = 0
    duration_seconds: int = 0
    instrumentalness: float = 0.0
    popularity: int = 0
    liveness: float = 0.0

@dataclass
class UserProfile:
    """
    Represents the user's taste preferences.
    Required by tests/test_recommender.py
    """

    # The defaults are None so when the user did not specify a certain preference,
    # the scoring function should skip it and renormalize the remaining weights.
    
    preferred_genres: Optional[List[str]] = None
    preferred_moods: Optional[List[str]] = None

    target_energy: Optional[float] = None
    target_tempo_bpm: Optional[float] = None
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None
    target_acousticness: Optional[float] = None
    target_instrumentalness: Optional[float] = None
    target_liveness: Optional[float] = None

    preferred_release_year: Optional[int] = None
    preferred_duration_seconds: Optional[int] = None
    target_popularity: Optional[int] = None
    

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file as a list of dictionaries."""

    songs = []

    integer_fields = [
        "id",
        "release_year",
        "duration_seconds",
        "popularity",
    ]

    float_fields = [
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "instrumentalness",
        "liveness",
    ]

    with open(
        csv_path,
        mode="r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file) # use the header row as dictionary keys
        
        # Convert CSV strings into appropriate numeric types then add each song dictionary to the list
        for row in reader:
            for field in integer_fields:
                row[field] = int(row[field])

            for field in float_fields:
                row[field] = float(row[field])

            songs.append(row)
            
        print(f"Loaded songs: {len(songs)}")
    return songs


def calculate_category_similarity(
    song_value: str,
    preferred_values: List[str],
    related_pairs: set,
) -> Tuple[float, str]: 
    """ Answer how closely does this song's category match the user's selected categories
    Return a tuple (similarity_number, explanation)"""

    normalized_song = song_value.strip().lower()

    normalized_preferences = [
        value.strip().lower()
        for value in preferred_values
    ]

    if normalized_song in normalized_preferences:
        return EXACT_SCORE, "exact category match"

    for preference in normalized_preferences:
        pair = frozenset((normalized_song, preference))

        if pair in related_pairs:
            return RELATED_SCORE, f"related to selected category '{preference}'"

    return UNRELATED_SCORE, "no category match"

def calculate_numeric_similarity(
    target: float,
    song_value: float,
    value_range: float = 1.0, 
) -> float:
    """Return a 0-1 similarity score based on normalized numeric distance."""
    
    difference = abs(target - song_value)
    similarity = 1.0 - difference / value_range
    return max(0.0, similarity)

def calculate_catalog_ranges(
    songs: List[Dict],
) -> Dict[str, float]:
    """Calculate normalization ranges from the current song catalog."""

    if not songs:
        raise ValueError(
            "Cannot calculate feature ranges from an empty catalog."
        )

    feature_ranges = {}

    for feature in DYNAMIC_RANGE_FEATURES:
        values = [
            song[feature]
            for song in songs
        ]

        minimum = min(values)
        maximum = max(values)

        observed_range = maximum - minimum
        
        # Used 1.0 to prevent dividing by zero
        feature_ranges[feature] = max(
            1.0,
            observed_range,
        )

    return feature_ranges

def score_song(user_prefs: Dict, song: Dict, feature_ranges: Dict[str, float]) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    feature_ranges contains the current catalog ranges for tempo, release year, and duration.
    """
    
    # Every active preference will add a tuple with this structure:
    # (feature_name, similarity, explanation)
    
    similarities = []
    
    # Calculate genre similarility 
    
    preferred_genres = user_prefs.get("preferred_genres")
    if preferred_genres:
        genre_similarity, genre_explanation = (
            calculate_category_similarity(
                song_value=song["genre"],
                preferred_values = preferred_genres,
                related_pairs = RELATED_GENRE_PAIRS,
            )
        )

        similarities.append(
            (
                "genre",
                genre_similarity,
                genre_explanation,
            )
        )
        
    # Calculate mood similarility 
    preferred_moods = user_prefs.get("preferred_moods")

    if preferred_moods:
        mood_similarity, mood_explanation = (
            calculate_category_similarity(
                song_value=song["mood"],
                preferred_values=preferred_moods,
                related_pairs=RELATED_MOOD_PAIRS,
            )
        )
        similarities.append(
            (
                "mood",
                mood_similarity,
                mood_explanation,
            )
        )

    # Calculate a normalized similarity for every active numeric preference.
    for (
        feature,
        preference_key,
        fixed_range,
        unit,
        decimal_places,
    ) in NUMERIC_FEATURE_CONFIG:
        target = user_prefs.get(preference_key)
        
        # If the user did not choose a preference, ignore
        if target is None: 
            continue
        
        if fixed_range is None:
            value_range = feature_ranges[feature] # E.g: tempo => value_range = feature_ranges["tempo_bpm"] = max - min
        else:
            value_range = fixed_range # E.g energy => value_range = fixed_range = 1.0


        similarity = calculate_numeric_similarity(
            target=target,
            song_value=song[feature],
            value_range=value_range,
        )

        target_display = f"{target:.{decimal_places}f}{unit}"
        song_display = f"{song[feature]:.{decimal_places}f}{unit}"

        similarities.append(
            (
                feature,
                similarity,
                (
                    f"target {target_display}, "
                    f"song value {song_display}"
                ),
            )
        )

    if not similarities:
        return 0.0, [
            "No active preferences were provided."
        ]

    active_weight = sum(
        FEATURE_WEIGHTS[feature]
        for feature, _, _ in similarities
    )

    weighted_total = sum(
        FEATURE_WEIGHTS[feature] * similarity
        for feature, similarity, _ in similarities
    )

    final_score = weighted_total / active_weight

    reasons = []

    for feature, similarity, explanation in similarities:
        normalized_weight = (
            FEATURE_WEIGHTS[feature]
            / active_weight
        )

        contribution = (
            normalized_weight
            * similarity
        )

        reasons.append(
            (
                f"{feature}: {explanation}; "
                f"similarity {similarity:.2f} x "
                f"normalized weight "
                f"{normalized_weight:.1%} = "
                f"contribution {contribution:.1%}"
            )
        )

    return final_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    
    if not songs or k <= 0:
        return []

    feature_ranges = calculate_catalog_ranges(songs)

    scored_songs = []

    for song in songs:
        score, reasons = score_song(
            user_prefs,
            song,
            feature_ranges,
        )

        explanation = "; ".join(reasons)

        scored_songs.append(
            (
                song,
                score,
                explanation,
            )
        )

    ranked_songs = sorted(
        scored_songs,
        key=lambda result: result[1],
        reverse=True,
    )

    return ranked_songs[:k]
