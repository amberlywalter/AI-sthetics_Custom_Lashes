def recommend_lash(eye_shape: str) -> str:
    """
    Return a recommended lash style based on detected eye shape.
    Includes default handling for unknown or mixed classifications.
    """

    recommendations = {
        "Almond Eyes": {
            "style": "Cat-Eye or Wispy Lash",
            "description": "Highlights natural symmetry with flared outer corners."
        },
        "Round Eyes": {
            "style": "Natural or Doll Lash",
            "description": "Opens the eyes with longer center lashes for a bright look."
        },
        "Balanced Eyes": {
            "style": "Classic or Hybrid Lash",
            "description": "Complements proportionate eye shapes with even volume."
        }
    }

    # Normalize input
    key = eye_shape.strip().title() if eye_shape else "Unknown"

    if key in recommendations:
        rec = recommendations[key]
        return f"{rec['style']} — {rec['description']}"
    else:
        # Default or fallback
        return "Custom Lash Style — tailored design based on client preferences."
