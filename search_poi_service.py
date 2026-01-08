
import re

filename = "Fortify_API_temp.html"
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

# Look for paths starting with /poi_service
matches = re.findall(r">(/poi_service[^<]*)<", content, re.IGNORECASE)

print(f"Found {len(matches)} matches:")
unique_matches = sorted(list(set(matches)))
for m in unique_matches:
    print(m)
