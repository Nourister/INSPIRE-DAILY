import sqlite3

# Function to search quotes by author or quote text
def search_quotes(search_term):
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()

    # Search query for quotes matching the search term
    c.execute("SELECT * FROM quotes WHERE author LIKE ? OR quote LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    results = c.fetchall()

    conn.close()

    return results

# Example usage:
search_term = input("Enter author name or quote text to search: ")
search_results = search_quotes(search_term)

if search_results:
    print(f"Search results for '{search_term}':")
    for result in search_results:
        print(f"Author: {result[1]}")
        print(f"Quote: {result[2]}\n")
else:
    print(f"No results found for '{search_term}'")