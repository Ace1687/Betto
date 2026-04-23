# tools.py

# -----------------------------
# Imports
# -----------------------------
from langchain_community.tools import DuckDuckGoSearchResults

# -----------------------------
# Tool Functions
# -----------------------------

def searchweb(parameters):
    """Search the web using DuckDuckGo (LangChain) and return top results."""
    print("searchweb called:", parameters)
    query = parameters.get("query")
    if not query:
        return "Error: 'query' parameter is missing."

    search = DuckDuckGoSearchResults()
    results = search.run(query)

    return results


def save_to_txt(parameters):
    """Save text data to a file."""
    print("save_to_txt called:", parameters)
    filename = parameters.get("filename")
    data = parameters.get("data")

    if not filename or not data:
        return "Error: 'filename' or 'data' parameter is missing."

    with open(filename, "a", encoding="utf-8") as file:
        file.write(data + "\n")

    return f"Saved to {filename}"


def create_html_file(parameters):
    """Create an HTML file with a title and content."""
    print("create_html_file called:", parameters)
    filename = parameters.get("filename")
    title = parameters.get("title", "No Title")
    data = parameters.get("data", "")

    if not filename or not title or not data:
        return "Error: 'filename', 'title', or 'data' parameter is missing."

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <div>{data}</div>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)

    return f"HTML file '{filename}' created successfully"

# -----------------------------
# Tool Manager
# -----------------------------
class ToolManager:
    def __init__(self):
        self.tools = []

    def register_tool(self, func, name, description):
        self.tools.append({
            "name": name,
            "function": func,
            "description": description
        })

# -----------------------------
# Register Tools
# -----------------------------
client_tools = ToolManager()

client_tools.register_tool(
    searchweb,
    "searchweb",
    "Search the web for information using DuckDuckGo (LangChain). Parameters: query (string)"
)

client_tools.register_tool(
    save_to_txt,
    "save_to_txt",
    "Save text data into a file. Parameters: filename (string), data (string)"
)

client_tools.register_tool(
    create_html_file,
    "create_html_file",
    "Create an HTML website with a title and content. Parameters: filename (string), title (string), data (string)"
)