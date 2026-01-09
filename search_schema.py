
filename = "Fortify_API.html"
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

# Search for poi_notes to see its definition
# It might be defined in a definition or schema section
import re

# Find occurrences of poi_notes and print context
matches = [m.start() for m in re.finditer('poi_notes', content)]

print(f"Found {len(matches)} occurrences of 'poi_notes'")

for i, index in enumerate(matches):
    print(f"--- OCCURRENCE {i+1} ---")
    start = max(0, index - 500)
    end = min(len(content), index + 1000) # Get more context after
    print(content[start:end])
    print("-----------------------")
