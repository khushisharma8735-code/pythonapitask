# User Directory Explorer

A beginner-friendly Python CLI application that fetches user records from a public REST API (`https://jsonplaceholder.typicode.com/users`), formats the response in a neat ASCII card layout, and provides interactive searching and filtering capabilities.

## Features

- **REST API Integration:** Uses `requests.get()` to pull user data.
- **Data Validation:** Verifies status codes using `.raise_for_status()` and safely parses the JSON payload.
- **Robust Error Handling:** Protects against network loss, timeouts, HTTP errors, and malformed JSON format.
- **Aesthetic Terminal UI:** Prints records formatted as aligned ASCII cards.
- **Interactive Multi-field Search:** Allows search/filtering by Name, Username, Email, and Company Name.
- **Interactive Loop Menu:** Keep searching or viewing all users until you decide to exit.

## Prerequisites

- Python 3.7+
- `requests` library

## Installation

1. Clone or download this project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the program directly from your terminal:

```bash
python main.py
```

### Menu Options
1. **Show All Users:** Displays all 10 users retrieved from the API.
2. **Search / Filter Users:** Prompts for a keyword (case-insensitive) and lists users whose Name, Username, Email, or Company contains that keyword.
3. **Exit:** Safely quits the program.

## Project Structure

- [main.py](file:///c:/myproject/pythonapitask/main.py): Contains all program logic (fetch, display, search, and menu loop).
- [requirements.txt](file:///c:/myproject/pythonapitask/requirements.txt): Lists external dependencies.
