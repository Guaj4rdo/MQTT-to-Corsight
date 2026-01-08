
filename = "Fortify_API_temp.html"
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

search_term = "/users_service/auth/login"
index = content.find(search_term)

if index != -1:
    print(f"Found '{search_term}' at index {index}")
    start = max(0, index - 500)
    end = min(len(content), index + 500)
    snippet = content[start:end]
    print("--- SNIPPET START ---")
    print(snippet)
    print("--- SNIPPET END ---")
else:
    print(f"'{search_term}' not found")
    
# Try searching for just "pois/"
search_term_2 = "pois/"
index2 = content.find(search_term_2)
if index2 != -1:
    print(f"Found '{search_term_2}' at index {index2}")
    start = max(0, index2 - 500)
    end = min(len(content), index2 + 500)
    snippet = content[start:end]
    print("--- SNIPPET 2 START ---")
    print(snippet)
    print("--- SNIPPET 2 END ---")
