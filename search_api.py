
filename = "Fortify_API_temp.html"
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

search_term = "AddPOIs"
index = content.find(search_term)

if index != -1:
    print(f"Found '{search_term}' at index {index}")
    # Print context around the match
    start = max(0, index - 1000)
    end = min(len(content), index + 5000)
    snippet = content[start:end]
    print("--- SNIPPET START ---")
    print(snippet)
    print("--- SNIPPET END ---")
else:
    print(f"'{search_term}' not found")

search_term_2 = "Create Pois"
index2 = content.find(search_term_2)
if index2 != -1:
    print(f"Found '{search_term_2}' at index {index2}")
    start = max(0, index2 - 1000)
    end = min(len(content), index2 + 5000)
    snippet = content[start:end]
    print("--- SNIPPET 2 START ---")
    print(snippet)
    print("--- SNIPPET 2 END ---")
