#!/usr/bin/env python3
"""
User Directory Explorer
-----------------------
A beginner-friendly Python CLI application that fetches user data from a public
REST API, parses the JSON response, and displays it in a clean, formatted layout.
It includes interactive filtering/searching features and robust error handling.

Requirements:
- requests (installed in environment)
"""

import sys
import requests

# The URL of the public REST API we want to fetch data from.
# This endpoint returns a list of 10 users with detailed contact and company info.
API_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_data(api_url: str) -> list | None:
    """
    Fetches JSON data from the specified API URL.

    Handles network issues, timeouts, HTTP errors, and invalid JSON responses
    gracefully, showing user-friendly messages.

    Args:
        api_url (str): The endpoint to send the GET request to.

    Returns:
        list: A list of dictionaries (records) on success.
        None: If the request fails or returns invalid data.
    """
    print(f"\n[~] Fetching data from: {api_url} ...")
    try:
        # Perform a GET request with a 10-second timeout to prevent the app from hanging.
        response = requests.get(api_url, timeout=10)

        # Validate the response status. If it's not a 2xx success code (e.g. 404, 500),
        # this will raise an HTTPError exception.
        response.raise_for_status()

        # Parse the JSON response.
        # This will raise a ValueError if the response is not valid JSON (e.g., raw HTML).
        data = response.json()

        # Ensure the response is in the expected list format.
        if not isinstance(data, list):
            print("[!] Error: Expected a list of records from the API, but got a different structure.")
            return None

        print("[+] Data fetched successfully!")
        return data

    except requests.exceptions.ConnectionError:
        print("[!] Network Error: Unable to connect to the server. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("[!] Timeout Error: The server took too long to respond. Please try again later.")
    except requests.exceptions.HTTPError as http_err:
        print(f"[!] HTTP Error: The server returned an error code: {response.status_code}")
        print(f"    Details: {http_err}")
    except ValueError:
        print("[!] Parsing Error: The response was not valid JSON data.")
    except requests.exceptions.RequestException as req_err:
        print(f"[!] Request Error: Something went wrong while fetching the data.")
        print(f"    Details: {req_err}")

    return None


def display_data(records: list) -> None:
    """
    Displays the list of records in a clean, human-readable terminal format.

    Uses standard ASCII characters to format the output like cards, ensuring
    maximum compatibility across all operating systems and terminal encodings.

    Args:
        records (list): List of user dictionaries to print.
    """
    if not records:
        print("\n+--------------------------------------------------------+")
        print("|                  No records to display.                |")
        print("+--------------------------------------------------------+")
        return

    print(f"\nShowing {len(records)} record(s):")
    
    # Loop through each record and display it using clean layout blocks
    for record in records:
        # Extract values with safe fallbacks (in case some keys are missing in the JSON)
        user_id = record.get("id", "N/A")
        name = record.get("name", "N/A")
        username = record.get("username", "N/A")
        email = record.get("email", "N/A")
        website = record.get("website", "N/A")
        
        # Company is a nested dictionary in our source API
        company_data = record.get("company", {})
        company_name = company_data.get("name", "N/A") if isinstance(company_data, dict) else "N/A"

        # Print a beautiful ASCII card for the user
        print("+--------------------------------------------------------+")
        print(f"|  ID: {user_id:<4} | Name: {name:<35}  |")
        print("+--------------------------------------------------------+")
        print(f"|  Username: {username:<42}  |")
        print(f"|  Email:    {email:<42}  |")
        print(f"|  Company:  {company_name:<42}  |")
        print(f"|  Website:  {website:<42}  |")
        print("+--------------------------------------------------------+")



def search_data(records: list, search_term: str) -> list:
    """
    Filters the records based on a search term.

    The search is case-insensitive and checks multiple fields:
    - Name
    - Username
    - Email
    - Company Name

    Args:
        records (list): The list of record dictionaries.
        search_term (str): The keyword to search for.

    Returns:
        list: Filtered list of records containing the search term.
    """
    # Clean the search term and make it lowercase for case-insensitive matching
    query = search_term.strip().lower()
    
    # If the search term is empty, return all records
    if not query:
        return records

    matching_records = []
    
    for record in records:
        # Get the fields we want to search in, fallback to empty string if missing
        name = str(record.get("name", "")).lower()
        username = str(record.get("username", "")).lower()
        email = str(record.get("email", "")).lower()
        
        # Get nested company name if exists
        company_data = record.get("company", {})
        company_name = ""
        if isinstance(company_data, dict):
            company_name = str(company_data.get("name", "")).lower()

        # Check if the query is a substring of any of these fields
        if (query in name or 
            query in username or 
            query in email or 
            query in company_name):
            matching_records.append(record)

    return matching_records


def print_menu() -> None:
    """
    Prints the interactive menu options.
    """
    print("\n" + "=" * 35)
    print("         MAIN MENU")
    print("=" * 35)
    print("  1. Show All Users")
    print("  2. Search / Filter Users")
    print("  3. Exit")
    print("=" * 35)


def main() -> None:
    """
    Main function to control the program flow and interactive menu.
    """
    print("==================================================")
    print("        WELCOME TO USER DIRECTORY EXPLORER")
    print("==================================================")

    # 1. Fetch data initially
    users = fetch_data(API_URL)

    # If data fetching fails completely on start, we cannot proceed.
    if users is None:
        print("\n[!] Critical Error: Could not fetch initial data.")
        print("    Please check your network and try running the program again.")
        sys.exit(1)

    # Display how many records were loaded
    print(f"\n[+] Loaded {len(users)} users from the API.")
    
    # 2. Show a few records initially as requested in the program flow
    initial_count = min(3, len(users))
    print(f"\nShowing first {initial_count} records to preview:")
    display_data(users[:initial_count])

    # 3. Enter interactive menu loop
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-3): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting program. Goodbye!")
            break

        if choice == "1":
            # Show all records
            display_data(users)

        elif choice == "2":
            # Search / Filter
            try:
                search_term = input("\nEnter search term (searches name, username, email, company): ")
            except (KeyboardInterrupt, EOFError):
                print("\nSearch cancelled.")
                continue

            results = search_data(users, search_term)
            
            if results:
                display_data(results)
            else:
                print(f"\n[!] No results found matching: '{search_term}'")

        elif choice == "3":
            print("\nExiting program. Thank you for using User Directory Explorer!")
            break

        else:
            print("\n[!] Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
