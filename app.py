import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_FILE = 'bucket_list.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Get query parameters
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    completed = request.args.get('completed', '').strip()
    sort_by = request.args.get('sort', 'id').strip()
    
    # Build query
    query = "SELECT * FROM bucket_list WHERE 1=1"
    params = []
    
    if search:
        query += " AND (title LIKE ? OR category LIKE ? OR location LIKE ?)"
        lk = f"%{search}%"
        params.extend([lk, lk, lk])
        
    if category:
        query += " AND category = ?"
        params.append(category)

    if completed == 'yes':
        query += " AND is_completed = 1"
    elif completed == 'no':
        query += " AND is_completed = 0"
        
    # Sort
    if sort_by == 'title':
        query += " ORDER BY title ASC"
    elif sort_by == 'age':
        query += " ORDER BY target_age ASC"
    elif sort_by == 'cost':
        query += " ORDER BY estimated_cost ASC"
    elif sort_by == 'completed':
        query += " ORDER BY is_completed ASC"
    else:  # default id
        query += " ORDER BY id DESC"

    # Execute main query
    items = conn.execute(query, params).fetchall()
    
    # Get distinct categories for the dropdown filter
    categories_rows = conn.execute('SELECT DISTINCT category FROM bucket_list WHERE category IS NOT NULL AND category != "" ORDER BY category').fetchall()
    categories = [row['category'] for row in categories_rows]
    
    conn.close()
    return render_template('index.html', items=items, categories=categories, 
                           search=search, current_category=category, 
                           completed=completed, sort_by=sort_by)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        target_age = request.form['target_age']
        estimated_cost = request.form['estimated_cost']
        location = request.form['location'] or None
        is_completed = 1 if 'is_completed' in request.form else 0

        # Basic validation handled by 'required' attribute in HTML but double checked here
        if not title or not category or not target_age or not estimated_cost:
            return redirect(url_for('index'))

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO bucket_list (title, category, target_age, estimated_cost, location, is_completed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, category, int(target_age), estimated_cost, location, is_completed))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM bucket_list WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        target_age = request.form['target_age']
        estimated_cost = request.form['estimated_cost']
        location = request.form['location'] or None
        is_completed = 1 if 'is_completed' in request.form else 0

        conn.execute('''
            UPDATE bucket_list 
            SET title = ?, category = ?, target_age = ?, estimated_cost = ?, location = ?, is_completed = ?
            WHERE id = ?
        ''', (title, category, int(target_age), estimated_cost, location, is_completed, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM bucket_list WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/toggle-complete/<int:id>', methods=('POST',))
def toggle_complete(id):
    conn = get_db_connection()
    item = conn.execute('SELECT is_completed FROM bucket_list WHERE id = ?', (id,)).fetchone()
    if item:
        new_status = 0 if item['is_completed'] else 1
        conn.execute('UPDATE bucket_list SET is_completed = ? WHERE id = ?', (new_status, id))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
