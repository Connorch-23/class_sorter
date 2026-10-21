import pandas as pd



def output_rosters(path, campers, classes):
    """Out puts the campers and classes into a master roster file."""
    rows = []
    for camper in campers:
        rows.append({
            'id': camper.id,
            'last_name': camper.last_name,
            'first_name': camper.first_name,
            'cabin': camper.cabin,
            **{period: section.parent_class_id for period, section in sorted(camper.enrolled_sections.items())},
            'score': round(camper.score, 2)
        })
    # Create DataFrame and export
    df = pd.DataFrame(rows)
    
    df.to_csv(path, index=False)
    