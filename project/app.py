import sqlite3 , books as bk
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
        conn = sqlite3.connect('bookSage.db')
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
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = sqlite3.connect('bookSage.db')
    cursor = conn.cursor()

    # Check if the user already submitted the survey
    cursor.execute('SELECT * FROM survey_responses WHERE user_id = ?', (user_id,))
    existing_response = cursor.fetchone()
    
    if request.method == 'POST':
        # Retrieve the form data from the survey
        reading_frequency = request.form.get('reading_frequency')
        book_preference = request.form.getlist('book_preference')
        discover_method = request.form.getlist('discover_method')
        genres = request.form.getlist('genres')
        fiction_non_fiction = request.form.get('fiction_non_fiction')
        explore_genres = request.form.get('explore_genres')
        tone = request.form.getlist('tone')
        themes = request.form.getlist('themes')
        book_length = request.form.get('book_length')
        book_era = request.form.getlist('book_era')
        narrative_perspective = request.form.get('narrative_perspective')
        favorite_authors = request.form.getlist('favorite_authors')
        top_books = request.form.getlist('top_books')
        reading_purpose = request.form.getlist('reading_purpose')
        thought_provoking = request.form.get('thought_provoking')

        # Format the multi-select fields as comma-separated strings
        book_preference_str = ', '.join(book_preference)
        discover_method_str = ', '.join(discover_method)
        genres_str = ', '.join(genres)
        tone_str = ', '.join(tone)
        themes_str = ', '.join(themes)
        book_era_str = ', '.join(book_era)
        favorite_authors_str = ', '.join(favorite_authors)
        top_books_str = ', '.join(top_books)
        reading_purpose_str = ', '.join(reading_purpose)

        if existing_response:
            # Update existing survey response
            cursor.execute('''
                UPDATE survey_responses
                SET reading_frequency = ?, book_preference = ?, discover_method = ?, genres = ?,
                    fiction_non_fiction = ?, explore_genres = ?, tone = ?, themes = ?, book_length = ?,
                    book_era = ?, narrative_perspective = ?, favorite_authors = ?, top_books = ?,
                    reading_purpose = ?, thought_provoking = ?
                WHERE user_id = ?
            ''', (
                reading_frequency, book_preference_str, discover_method_str, genres_str,
                fiction_non_fiction, explore_genres, tone_str, themes_str, book_length,
                book_era_str, narrative_perspective, favorite_authors_str, top_books_str,
                reading_purpose_str, thought_provoking, user_id
            ))
        else:
            # Insert new survey response
            cursor.execute('''
                INSERT INTO survey_responses (
                    user_id, reading_frequency, book_preference, discover_method, genres,
                    fiction_non_fiction, explore_genres, tone, themes, book_length, book_era,
                    narrative_perspective, favorite_authors, top_books, reading_purpose, thought_provoking
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, reading_frequency, book_preference_str, discover_method_str, genres_str,
                fiction_non_fiction, explore_genres, tone_str, themes_str, book_length, book_era_str,
                narrative_perspective, favorite_authors_str, top_books_str, reading_purpose_str, thought_provoking
            ))

        # Mark user as completed survey
        cursor.execute('UPDATE users SET has_completed_survey = 1 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

        flash("Survey submitted successfully! You can review or update your answers on your dashboard.", "success")
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('survey.html')

@app.route('/survey_review')
def survey_review():
    # Assuming you're logged in and have a user_id available
    user_id = session['user_id']  # Replace with actual method to get the user_id
    
    # Fetch the survey responses for the current user
    conn = sqlite3.connect('bookSage.db')
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
            conn = sqlite3.connect('bookSage.db')
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

    conn = sqlite3.connect('bookSage.db')
    c = conn.cursor()

    # Get user personal info
    c.execute("SELECT first_name, last_name, email FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()

    # Get books the user has saved
    c.execute('''
        SELECT b.Title, b.ISBN, b.Pubdate, b.Genre
        FROM user_books ub
        JOIN books b ON ub.isbn = b.ISBN
        WHERE ub.user_id = ?
    ''', (session['user_id'],))
    saved_books = c.fetchall()

    conn.close()

    return render_template('profile.html', user=user, saved_books=saved_books)


# dashboard route
#<!--that was added or modify-->
# Define the function to check survey completion
def check_if_completed_survey(user_id):
    conn = sqlite3.connect('bookSage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT has_completed_survey FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0] == 1  # Assuming 1 means survey completed
    return False

# Dashboard route
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = sqlite3.connect('bookSage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, last_name FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return redirect(url_for('login'))  # If no user is found, redirect to login

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
        # connect to bookSage database
        db = bk.db_connection()

    # query Books table to display info on books
    books = bk.query_table(db)


    # call function to get user's id to display on web page
    user = bk.get_user_by_id(session['user_id'])  

    return render_template('allbooks.html', books = books, user = user)
def add_book_to_profile(user_id, isbn):
    conn = sqlite3.connect('bookSage.db')
    cursor = conn.cursor()

    # Check if the book is already saved
    cursor.execute('SELECT 1 FROM user_books WHERE user_id = ? AND isbn = ?', (user_id, isbn))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute('INSERT INTO user_books (user_id, isbn) VALUES (?, ?)', (user_id, isbn))
        conn.commit()

    conn.close()


# displays full details about one single book
@app.route('/book/<isbn>', methods=['GET', 'POST'])
def book_detail(isbn):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    connection = bk.db_connection()
    book = bk.get_book_by_isbn(connection, isbn)
    user = bk.get_user_by_id(user_id)

    if not book:
        return render_template('404.html'), 404

    # Check if the book is already saved
    conn = sqlite3.connect('bookSage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM user_books WHERE user_id = ? AND isbn = ?', (user_id, isbn))
    already_saved = cursor.fetchone() is not None
    conn.close()

    if request.method == 'POST' and not already_saved:
        add_book_to_profile(user_id, isbn)
        return redirect(url_for('book_detail', isbn=isbn))

    return render_template('book_detail.html', book=book, user=user, already_saved=already_saved)

@app.route('/recommendations')
def recommendations():
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user_id = session['user_id']

    try:
        # Get user's selected genres from database.db
        conn_user = sqlite3.connect('bookSage.db')
        user_cursor = conn_user.cursor()
        user_cursor.execute("SELECT genres FROM survey_responses WHERE user_id = ?", (user_id,))
        row = user_cursor.fetchone()
        conn_user.close()

        if not row or not row[0]:
            return jsonify({'message': 'No survey found or no genres selected.'})

        genres = [g.strip() for g in row[0].split(',')]

        # Get matching books from books.db
        conn_books = sqlite3.connect('bookSage.db')
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
