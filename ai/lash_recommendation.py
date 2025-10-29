def recommend_lash(eye_shape):
    recommendations = {
        "Almond Eyes": "Cat-Eye or Wispy Lash",
        "Round Eyes": "Natural or Doll Lash",
        "Balanced Eyes": "Classic or Hybrid Lash"
    }
    return recommendations.get(eye_shape, "Custom Lash Style")
