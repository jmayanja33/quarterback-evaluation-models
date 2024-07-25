"""
These edits are for the normalized K-means clusters with k = 6

Quarterback Clusters:
    - 0: Starters
    - 1: Practice Squad
    - 2: Fringe Starters/Backups
    - 3: High-End Mobile Quarterbacks
    - 4: Elite Hall of Fame Quarterbacks
    - 5: High-End Pocket Passers
"""


# Dictionary to optimize clusters
edits = {
    "Patrick Mahomes": 3,       # Patrick Mahomes, cluster 0 --> 3
    "Justin Herbert": 0,        # Justin Herbert, cluster 2 --> 0
    "Andrew Luck": 5,           # Andrew Luck, cluster 0 --> 5
    "Brock Purdy": 0,           # Brock Purdy, cluster 2 --> 0
    "Mason Rudolph": 2,         # Mason Rudolph, cluster 1 --> 2
    "Robert Griffin III": 3,    # Robert Griffin III, cluster 4 --> 5
    "Joe Burrow": 5,            # Joe Burrow, cluster 2 --> 5
    "Deshaun Watson": 3,        # Deshaun Watson, cluster 2 --> 3
    "Dak Prescott": 3,          # Dak Prescott, cluster 0 --> 3
    "Joshua Dobbs": 2,          # Josh Dobbs, cluster 1 --> 2
    "Jalen Hurts": 3,           # Jalen Hurts, cluster 2 --> 3
}