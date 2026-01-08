
import re

filename = "Fortify_API_temp.html"
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

# Regex to find paths in the HTML
# Looking for /...pois...
# The example showed: >/users_service/auth/login/<
# So looking for >/[^<]*pois[^<]*<
matches = re.findall(r">(/[^<]*pois[^<]*)<", content, re.IGNORECASE)

print(f"Found {len(matches)} matches:")
for m in matches:
    print(m)
