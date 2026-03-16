#  Bucket List App
This is a simple bucket list app that allows me to add, view, update, and delete items from my list. I built it to make updating my goals quick and easy, while also keeping the interface clean and visually appealing—unlike a notes app or spreadsheet—so it’s something I actually want to check frequently.

## About the database
I created 1 table in the database called `bucket_list`.
It has the following columns:
    - `id` (integer primary key): unique identifer for each entry
    - `title` (string): the description of the bucket list item
    - `category` (string): the category of the bucket list item
    - `target_age` (integer): the age I want to have completed the bucket list item by
    - `estimated_cost` (string with options "low", "medium", "high", "super high"): the estimated cost of the bucket list item
    - `location` (string): the location of the bucket list item, if any. Can be left empty
    - `is_completed` (boolean of "y" or "n"): whether the bucket list item is completed

## Key Features
- Supports input via terminal commands OR a web app
- Preserves your position on the page when searching or filtering, so I do not have to scroll back down each time.
- Follows the same aesthetics as my personal website (https://rionkuri22.github.io/), including a dark-mode interface
- Ensures I have access to my bucket list for life without reluing on any external hosting services!

## How to perform the CRUD operations
Create
- CLI: Choose option 1 from menu. As prompted, enter Title, Category, Age, Estimated Cost, Location, and whether it is completed.
- Web UI: Use the "Add a New Goal" card at the top of the interface. Fill in the fields and click the "Add to List ↗" button.

Read
- CLI: Choose option 1 from menu. Follow prompts to view the entire list, or filter and sort it by the different columns
- Web UI: The full list is shown by default. Use the search bar and the options on the left to filter and sort by different columns.

Update 
- CLI: Choose option 3 from menu. Input id of the entry you want to update and follow instructions
- Web UI: Click the edit icon (book with pencil) on any goal card. Make any changes in the popup window. Click "Save Changes" to finish.

Delete
- CLI: Choose option 4 from menu. Input id of the entry you want to delete and follow instructions
- Web UI: Click the trash can icon on any goal card. A confirmation popup will appear. Click "Delete" to finish.

## How to run
Option A: Terminal (CLI)
- Open the terminal in the project folder
- Run the command: python3 tracker/bucket_list.py
- Follow the menu to perform the CRUD operations
- When finished, 5 to end session

Option B: Web Interface (Flask app)
- Open the terminal in the project folder
- (IF not already installed): Run the command: pip3 install flask
- Run the command: python3 app.py
- Go to the URL in your browser of choice: http://127.0.0.1:5000/
- When finished, CTRL + C to stop the server