import sqlite3 , books as bk
# Note: Took out models - need to add it back in?
from flask import Flask, render_template, request, redirect, url_for, flash, session, g,jsonify # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore

app = Flask(__name__)
app.secret_key = 'supersecretkey'


# Home route (mainPage)
@app.route('/')
def index():
    return render_template('mainPage.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[4], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))
    return render_template('login.html')
# Survey route <!--that was added or modify-->
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':
        user_id = session['user_id']

        # Gather form data
        reading_frequency = request.form.get('reading_frequency')
        book_preference = ', '.join(request.form.getlist('book_preference'))
        discover_method = ', '.join(request.form.getlist('discover_method'))
        genres = ', '.join(request.form.getlist('genres'))
        other_genre = request.form.get('genre')
        if other_genre:
            genres += f", {other_genre}"
        fiction_non_fiction = request.form.get('fiction_non_fiction')
        explore_genres = request.form.get('explore_genres')
        tone = ', '.join(request.form.getlist('tone'))
        themes = ', '.join(request.form.getlist('themes'))
        book_length = request.form.get('book_length')
        book_era = ', '.join(request.form.getlist('book_era'))
        narrative_perspective = request.form.get('narrative_perspective')
        favorite_authors = ', '.join(request.form.getlist('favorite_authors'))
        top_books = ', '.join(request.form.getlist('top_books'))
        reading_purpose = ', '.join(request.form.getlist('reading_purpose'))
        thought_provoking = request.form.get('thought_provoking')

        # Check if this user already submitted survey
        c.execute("SELECT * FROM survey_responses WHERE user_id = ?", (user_id,))
        existing = c.fetchone()

        if existing:
            # Update existing response
            c.execute("""
                UPDATE survey_responses SET
                    reading_frequency = ?, book_preference = ?, discover_method = ?, genres = ?, fiction_non_fiction = ?,
                    explore_genres = ?, tone = ?, themes = ?, book_length = ?, book_era = ?, narrative_perspective = ?,
                    favorite_authors = ?, top_books = ?, reading_purpose = ?, thought_provoking = ?
                WHERE user_id = ?
            """, (
                reading_frequency, book_preference, discover_method, genres, fiction_non_fiction,
                explore_genres, tone, themes, book_length, book_era, narrative_perspective,
                favorite_authors, top_books, reading_purpose, thought_provoking, user_id
            ))
        else:
            # Insert new response
            c.execute("""
                INSERT INTO survey_responses (
                    user_id, reading_frequency, book_preference, discover_method, genres, fiction_non_fiction,
                    explore_genres, tone, themes, book_length, book_era, narrative_perspective,
                    favorite_authors, top_books, reading_purpose, thought_provoking
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, reading_frequency, book_preference, discover_method, genres, fiction_non_fiction,
                explore_genres, tone, themes, book_length, book_era, narrative_perspective,
                favorite_authors, top_books, reading_purpose, thought_provoking
            ))

        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))  # Or any other page

    else:
        # If GET request, optionally pre-fill the form for editing
        user_id = session['user_id']
        c.execute("SELECT * FROM survey_responses WHERE user_id = ?", (user_id,))
        data = c.fetchone()
        conn.close()
        return render_template('survey.html', data=data)
        
@app.route('/survey_review')
def survey_review():
    # Assuming you're logged in and have a user_id available
    user_id = session['user_id']  # Replace with actual method to get the user_id
    
    # Fetch the survey responses for the current user
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    cursor = conn.cursor()

    # Query to get the user's survey responses
    cursor.execute("SELECT * FROM survey_responses WHERE user_id = ?", (user_id,))
    survey_responses = cursor.fetchone()

    conn.close()

    return render_template('survey_review.html', survey_responses=survey_responses)


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='scrypt')
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
                          (first_name, last_name, email, hashed_password))
                conn.commit()
                flash('Registration successful! Please login.')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Email already exists.')
                return redirect(url_for('register'))
            finally:
                conn.close()
        else:
            flash('Passwords do not match.')
            return redirect(url_for('register'))
    return render_template('register.html')

# Profile route
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT first_name, last_name, email FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    conn.close()
    return render_template('profile.html', user=user)

# dashboard route
#<!--that was added or modify-->
@app.route('/dashboard')
def dashboard():
    # Retrieve the user id from the session
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    # Fetch the user details from the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, last_name FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    # Check if the user exists
    if not user:
        return redirect(url_for('login'))

    # Check if the user has completed the survey
    has_completed_survey = check_if_completed_survey(user_id)

    # Render the dashboard page with the user details and survey status
    return render_template('dashboard.html', user=user, has_completed_survey=has_completed_survey)


# display all books in database
@app.route('/allbooks')
def all_books():
    # make sure user is logged in first

    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'db' not in g:
        # connect to books database
        db = bk.db_connection()
    # query Books table to display info on books
    books = bk.query_table(db)

    # store user info in session (or fetch from DB?)
    user = session.get('user')

    return render_template('allbooks.html', books = books, user = user)
    
    


def check_if_completed_survey(user_id):
    # Check if the user has completed the survey
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT has_completed_survey FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == 1  # Assuming 1 means the survey is completed
@app.route('/recommendations')
def recommendations():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user_id = session['user_id']

    try:
        # Get user's selected genres from database.db
        conn_user = sqlite3.connect('database.db')
        user_cursor = conn_user.cursor()
        user_cursor.execute("SELECT genres FROM survey_responses WHERE user_id = ?", (user_id,))
        row = user_cursor.fetchone()
        conn_user.close()

        if not row or not row[0]:
            return jsonify({'message': 'No survey found or no genres selected.'})

        genres = [g.strip() for g in row[0].split(',')]

        # Get matching books from books.db
        conn_books = sqlite3.connect('books.db')
        books_cursor = conn_books.cursor()
        placeholders = ','.join('?' for _ in genres)
        query = f"SELECT Title, ISBN, Pubdate, Genre FROM books WHERE Genre IN ({placeholders})"
        books_cursor.execute(query, genres)
        books = books_cursor.fetchall()
        conn_books.close()

        if not books:
            return jsonify({'message': 'No books found for your preferences.'})

        recommendations = [
            {'Title': title, 'ISBN': isbn, 'Pubdate': pubdate, 'Genre': genre}
            for title, isbn, pubdate, genre in books
        ]
        return jsonify(recommendations)

    except Exception as e:
        print("Error:", e)
        return jsonify({'message': 'An error occurred while fetching recommendations.'}), 500

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))  # Redirects to the home page

if __name__ == '__main__':
    app.run(debug=True)
