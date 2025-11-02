def recommend_lash(analysis):
    """
    Takes structured output from shape_analysis.py and returns a detailed
    lash mapping plan aligned with professional lash technician practices.
    """

    eye_shape = analysis.get("eye_shape", "Unknown")
    eyelid_exposure = analysis.get("eyelid_exposure", "Moderate")
    projection_type = analysis.get("projection_type", "Average Depth")
    symmetry = analysis.get("symmetry_score", "Balanced")
    openness = analysis.get("openness_mm", 8.0)
    tilt = analysis.get("tilt_angle_deg", 0.0)

    # --- Base style by shape ---
    base_styles = {
        "Almond Eyes": "Cat-Eye or Natural Sweep",
        "Round Eyes": "Dolly or Open-Eye",
        "Monolid (Low Eyelid Crease)": "Dolly or Gradual Lift",
        "Downturned / Upturned Eyes": "Cat-Eye Lift",
        "Balanced Eyes": "Hybrid or Classic Map"
    }

    base_descriptions = {
        "Almond Eyes": "Enhances natural symmetry and elongates outer corners.",
        "Round Eyes": "Opens up and balances the roundness with upward length.",
        "Monolid (Low Eyelid Crease)": "Adds visible curl and depth to create lift.",
        "Downturned / Upturned Eyes": "Balances asymmetry with lifted outer corners.",
        "Balanced Eyes": "Maintains harmony with soft gradient length transitions."
    }

    style = base_styles.get(eye_shape, "Custom Lash Map")
    description = base_descriptions.get(eye_shape, "Tailored through facial analysis.")

    # --- Dynamic Curls based on projection and lid space ---
    if eyelid_exposure == "Low" or projection_type == "Deep Set":
        curl = "L or M Curl"  # lifts lashes out of deep socket
    elif eyelid_exposure == "High" or projection_type == "Projected / Prominent":
        curl = "C Curl"  # moderate lift to prevent excessive curl
    else:
        curl = "CC or D Curl"  # balanced for average lid space

    # --- Adjust lengths based on openness and symmetry ---
    if openness < 6:
        length_range = "8–10 mm"  # smaller eyes, conservative length
    elif openness < 9:
        length_range = "9–12 mm"
    else:
        length_range = "10–13 mm"  # larger or open eyes

    # Adjust for symmetry: balance if one side lower/higher
    if "Asymmetry" in symmetry:
        description += " Adjust lengths slightly to balance corner height differences."

    # --- Outer corner angle adjustments ---
    if tilt > 3:
        style += " (Lifting emphasis on outer corners)"
    elif tilt < 1:
        style += " (Soft even mapping)"

    # --- Build final structured plan ---
    return {
        "eye_shape": eye_shape,
        "recommended_style": style,
        "description": description,
        "recommended_curl": curl,
        "recommended_lengths_mm": length_range,
        "notes": f"{projection_type}, {eyelid_exposure} lid exposure, {symmetry} alignment"
    }
