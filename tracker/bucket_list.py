import sqlite3

def init_db():
    con = sqlite3.connect('bucket_list.db')
    cur = con.cursor()
    # Using TEXT for estimated_cost to support "low", "medium", etc.
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bucket_list (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            target_age INTEGER NOT NULL,
            estimated_cost TEXT NOT NULL,
            location TEXT,
            is_completed BOOLEAN NOT NULL
        )
    ''')
    con.commit()
    con.close()

def insert_bucket_list_item():
    print("\n--- Add a New Bucket List Item ---")
    title = input("Enter title (required): ").strip()
    while not title:
        title = input("Title cannot be blank. Enter title: ").strip()

    category = input("Enter category (required): ").strip()
    while not category:
        category = input("Category cannot be blank. Enter category: ").strip()
    
    target_age_input = input("Enter target age (required): ").strip()
    while not target_age_input.isdigit():
        target_age_input = input("Please enter a valid number for target age: ").strip()
    target_age = int(target_age_input)
    
    print("Cost options: low, medium, high, super high")
    estimated_cost = input("Enter estimated cost (required): ").strip().lower()
    while not estimated_cost:
        estimated_cost = input("Estimated cost cannot be blank. Enter estimated cost: ").strip().lower()
    
    location = input("Enter location (or leave blank): ").strip()
    if not location:
        location = None
    
    is_completed_input = input("Is it completed? (y/n): ").strip().lower()
    is_completed = is_completed_input in ['y', 'yes', 'true']

    con = sqlite3.connect('bucket_list.db')
    cur = con.cursor()

    sql = '''
        INSERT INTO bucket_list 
        (title, category, target_age, estimated_cost, location, is_completed)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    
    try:
        cur.execute(sql, (title, category, target_age, estimated_cost, location, is_completed))
        con.commit()
        print(f"\nSuccessfully added '{title}' to your bucket list!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

def view_bucket_list():
    print("\n--- View/Search Bucket List ---")
    search_keyword = input("Search keyword (Search title/category/location, blank for all): ").strip()
    
    filter_cat = input("Filter by Category (blank for all): ").strip()
    filter_done = input("Filter by Completed? (y/n, blank for all): ").strip().lower()
    
    print("\nSort by: 1. Title, 2. Age, 3. Cost Level, 4. Completion, 5. ID")
    sort_choice = input("Choice (default 5): ")
    
    order_by = "id"
    if sort_choice == "1": order_by = "title"
    elif sort_choice == "2": order_by = "target_age"
    elif sort_choice == "3": order_by = "estimated_cost"
    elif sort_choice == "4": order_by = "is_completed"

    con = sqlite3.connect('bucket_list.db')
    cur = con.cursor()

    query = "SELECT * FROM bucket_list WHERE 1=1"
    params = []

    if search_keyword:
        query += " AND (title LIKE ? OR category LIKE ? OR location LIKE ?)"
        lk = f"%{search_keyword}%"
        params.extend([lk, lk, lk])

    if filter_cat:
        query += " AND category = ?"
        params.append(filter_cat)

    if filter_done in ['y', 'yes']:
        query += " AND is_completed = 1"
    elif filter_done in ['n', 'no']:
        query += " AND is_completed = 0"

    query += f" ORDER BY {order_by}"

    try:
        cur.execute(query, params)
        rows = cur.fetchall()
        
        if not rows:
            print("\nNo items found matching your criteria.")
            return

        print(f"\n{'ID':<4} {'Title':<20} {'Category':<15} {'Age':<5} {'Cost':<12} {'Loc':<15} {'Done':<5}")
        print("-" * 82)
        for row in rows:
            is_done = "Yes" if row[6] else "No"
            print(f"{row[0]:<4} {row[1]:<20} {row[2]:<15} {row[3] if row[3] else 'N/A':<5} {row[4] if row[4] else 'N/A':<12} {row[5] if row[5] else 'N/A':<15} {is_done:<5}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

def main_menu():
    init_db()
    while True:
        print("\n=== Bucket List CLI ===")
        print("1. Add Item")
        print("2. View List (Sort/Filter)")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            insert_bucket_list_item()
        elif choice == "2":
            view_bucket_list()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main_menu()
