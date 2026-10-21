import pandas as pd



def output_rosters(path, campers, classes):
    """Out puts the campers and classes into a master roster file."""
    rows = []
    for camper in campers:
        score = 0.0
        for section in camper.enrolled_sections.values():
            if section.parent_class_id in camper.preferences:
                # Rank 0 (1st choice) -> score 1.0
                # Rank 1 (2nd choice) -> score 0.5
                # Rank 2 (3rd choice) -> score 0.33
                rank_index = camper.preferences.index(section.parent_class_id)
                score += 1.0 / (rank_index + 1)
            else:
                # No preference match adds nothing to the score
                score += 0.0

        rows.append({
            'id': camper.id,
            'last_name': camper.last_name,
            'first_name': camper.first_name,
            'cabin': camper.cabin,
            **{period: section.parent_class_id for period, section in sorted(camper.enrolled_sections.items())},
            'score': round(score, 2)
        })
    # Create DataFrame and export
    df = pd.DataFrame(rows)
    
    df.to_csv(path, index=False)
    