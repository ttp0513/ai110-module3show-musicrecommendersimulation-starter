from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

# Proposed weights in the recommender system
FEATURE_WEIGHTS = {
    "genre": 0.20,
    "mood": 0.20,
    "energy": 0.12,
    "tempo_bpm": 0.08,
    "valence": 0.08,
    "danceability": 0.08,
    "acousticness": 0.08,
    "instrumentalness": 0.06,
    "release_year": 0.05,
    "duration_seconds": 0.05,
}

EXACT_SCORE = 1.0
RELATED_SCORE = 0.5
UNRELATED_SCORE = 0


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

    preferred_release_year: Optional[int] = None
    preferred_duration_seconds: Optional[int] = None
    

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
    ]

    float_fields = [
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "instrumentalness",
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
    """ Answer how closely does this song's category match the user's selected categories'
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


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    
    # Every active preference will add a tuple with this structure:
    # (feature_name, similarity, explanation)
    
    similarities = []

    # TODO: Calculate genre similarity.
    # Add ("genre", similarity, explanation) when genre is active.

    # TODO: Calculate mood similarity.
    # Add ("mood", similarity, explanation) when mood is active.

    target_energy = user_prefs.get("target_energy")

    if target_energy is not None:
        energy_similarity = max(
            0.0,
            1.0 - abs(
                target_energy - song["energy"]
            ),
        )

        similarities.append(
            (
                "energy",
                energy_similarity,
                (
                    f"energy {song['energy']:.2f} is close to "
                    f"target {target_energy:.2f}"
                ),
            )
        )

    # TODO: Add tempo similarity using a range of 142 BPM.
    # TODO: Add valence similarity.
    # TODO: Add danceability similarity.
    # TODO: Add acousticness similarity.
    # TODO: Add instrumentalness similarity.
    # TODO: Add release-year similarity using a range of 14 years.
    # TODO: Add duration similarity using a range of 449 seconds.

    if not similarities:
        return 0.0, ["No active preferences were provided."]

    active_weight = sum(
        FEATURE_WEIGHTS[feature]
        for feature, similarity, explanation in similarities
    )

    weighted_total = sum(
        FEATURE_WEIGHTS[feature] * similarity
        for feature, similarity, explanation in similarities
    )

    final_score = weighted_total / _____

    reasons = []

    for feature, similarity, explanation in similarities:
        normalized_contribution = (
            FEATURE_WEIGHTS[feature]
            * similarity
            / active_weight
        )

        reasons.append(
            (
                f"{feature}: {explanation}; "
                f"similarity {similarity:.2f} × "
                f"weight {FEATURE_WEIGHTS[feature]:.0%} "
                f"= {normalized_contribution:.1%} of final score"
            )
        )

    return _____, _____

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
