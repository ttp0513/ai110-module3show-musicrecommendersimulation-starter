from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        preferred_genres=["pop"],
        preferred_moods=["happy"],
        target_energy=0.8,
    )
    rec = make_small_recommender()

    # Reverse the catalog so this test verifies scoring, not input order.
    rec.songs.reverse()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        preferred_genres=["pop"],
        preferred_moods=["happy"],
        target_energy=0.8,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "Match score:" in explanation
    assert "genre:" in explanation
    assert "mood:" in explanation


def test_recommend_handles_empty_catalog_and_non_positive_k():
    user = UserProfile(preferred_genres=["pop"])

    assert Recommender([]).recommend(user, k=5) == []
    assert make_small_recommender().recommend(user, k=0) == []
