"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import re
import sys
from textwrap import fill

from .recommender import FEATURE_WEIGHTS, load_songs, recommend_songs


REASON_PATTERN = re.compile(
    r"^(?P<feature>[^:]+): (?P<explanation>.*); "
    r"similarity (?P<similarity>[\d.]+) x normalized weight "
    r"(?P<importance>[\d.]+)% = contribution "
    r"(?P<contribution>[\d.]+)%$"
)


def format_feature_name(feature: str) -> str:
    """Convert an internal feature key into a readable label."""

    labels = {
        "tempo_bpm": "Tempo",
        "duration_seconds": "Duration",
        "release_year": "Release year",
    }
    return labels.get(feature, feature.replace("_", " ").capitalize())


def human_friendly_match(
    feature,
    explanation,
    similarity,
    song,
    user_prefs,
):
    """Translate one technical match into a summary and optional detail."""

    if feature in {"genre", "mood"}:
        song_value = str(song[feature]).title()
        preference_key = (
            "preferred_genres"
            if feature == "genre"
            else "preferred_moods"
        )
        selected_values = [
            str(value).title()
            for value in user_prefs.get(preference_key, [])
        ]
        selected_value = join_feature_names(selected_values)

        if explanation == "exact category match":
            return (
                f"{song_value} matches your {selected_value} preference",
                None,
            )

        if explanation.startswith("related to selected category"):
            selected_value = explanation.split("'", 2)[1].title()
            return (
                f"{song_value} is related to your {selected_value} preference",
                None,
            )

        return (
            f"{song_value} does not match your {selected_value} preference",
            None,
        )

    if similarity >= 0.95:
        summary = "Very close to your target"
    elif similarity >= 0.80:
        summary = "Close to your target"
    elif similarity >= 0.60:
        summary = "Somewhat close to your target"
    else:
        summary = "Far from your target"

    numeric_match = re.fullmatch(
        r"target (.*), song value (.*)",
        explanation,
    )
    detail = None
    if numeric_match:
        detail = (
            f"You requested {numeric_match.group(1)}; "
            f"this song is {numeric_match.group(2)}"
        )

    return summary, detail


def parse_reason(reason):
    """Extract display fields from one reason returned by score_song()."""

    match = REASON_PATTERN.fullmatch(reason)
    if not match:
        return None

    return {
        "feature": match.group("feature"),
        "explanation": match.group("explanation"),
        "similarity": float(match.group("similarity")),
        "importance": float(match.group("importance")),
        "contribution": float(match.group("contribution")),
    }


def join_feature_names(names):
    """Join feature labels into a readable English list."""

    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{', '.join(names[:-1])}, and {names[-1]}"

def main() -> None:
    """Load a sample profile and print its ranked song recommendations."""

    # Use UTF-8 so Windows terminals can display the recommendation checkmarks.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    songs = load_songs("data/songs.csv")

    # Example profile using the preference names expected by score_song().
    user_prefs = {
        "preferred_genres": ["pop"],
        "preferred_moods": ["happy"],
        "target_energy": 0.8,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 72)
    print("TOP MUSIC RECOMMENDATIONS")
    print("=" * 72)

    if not recommendations:
        print("No recommendations are available for this profile.")
        return

    for rank, (song, score, explanation) in enumerate(
        recommendations,
        start=1,
    ):
        reason_details = [
            parsed
            for reason in explanation.splitlines()
            if (parsed := parse_reason(reason)) is not None
        ]

        print(f"\n{rank}. {song['title']} - {song['artist']}")
        print(
            f"   Genre: {song['genre'].title()} | "
            f"Mood: {song['mood'].title()}"
        )
        print(f"   Match score: {score * 100:.1f} / 100")
        print("\n   Why we recommended it:")

        for detail in reason_details:
            summary, extra_detail = human_friendly_match(
                detail["feature"],
                detail["explanation"],
                detail["similarity"],
                song,
                user_prefs,
            )
            label = format_feature_name(detail["feature"])
            if detail["similarity"] >= 0.80:
                marker = "✓"
            elif detail["similarity"] > 0:
                marker = "~"
            else:
                marker = "✗"
            print(f"     {marker} {label}: {summary}")
            if extra_detail:
                print(f"       {extra_detail}")

        active_features = [
            format_feature_name(detail["feature"])
            for detail in reason_details
        ]
        active_features = [
            name if index == 0 else name.lower()
            for index, name in enumerate(active_features)
        ]
        print(f"\n   Based on: {join_feature_names(active_features)}")

        inactive_features = [
            format_feature_name(feature)
            for feature in FEATURE_WEIGHTS
            if feature not in {
                detail["feature"] for detail in reason_details
            }
        ]
        if inactive_features:
            inactive_features = [
                name if index == 0 else name.lower()
                for index, name in enumerate(inactive_features)
            ]
            print(
                fill(
                    f"Not considered: {join_feature_names(inactive_features)}",
                    width=72,
                    initial_indent="   ",
                    subsequent_indent="     ",
                )
            )

        print("\n   How the score was calculated:\n")
        print(
            f"   {'Factor':<16}{'Match':>8}"
            f"{'Importance':>14}{'Score points':>16}"
        )
        print("   " + "-" * 54)

        for detail in reason_details:
            label = format_feature_name(detail["feature"])
            print(
                f"   {label:<16}"
                f"{detail['similarity']:>7.0%}"
                f"{detail['importance']:>13.1f}%"
                f"{detail['contribution']:>16.1f}"
            )

        print("   " + "-" * 54)
        print(f"   {'Final score':<38}{score * 100:>16.1f} / 100")

        print("   " + "-" * 69)

    print()


if __name__ == "__main__":
    main()
