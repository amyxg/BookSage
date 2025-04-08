import sqlite3 , models, books as bk
from flask import Flask, render_template, request, redirect, url_for, flash, session # type: ignore
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
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in

    user_id = session['user_id']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Check if the user already completed the survey
    c.execute("SELECT * FROM survey WHERE user_id = ?", (user_id,))
    existing_survey = c.fetchone()
    
    if request.method == 'POST':
        favorite_genres = request.form['favorite_genres']
        favorite_authors = request.form['favorite_authors']
        fiction_or_nonfiction = request.form['fiction_or_nonfiction']
        
        if existing_survey:
            # Update existing survey
            c.execute('''
                UPDATE survey 
                SET favorite_genres = ?, favorite_authors = ?, fiction_or_nonfiction = ?
                WHERE user_id = ?
            ''', (favorite_genres, favorite_authors, fiction_or_nonfiction, user_id))
        else:
            # Insert new survey data
            c.execute('''
                INSERT INTO survey (user_id, favorite_genres, favorite_authors, fiction_or_nonfiction)
                VALUES (?, ?, ?, ?)
            ''', (user_id, favorite_genres, favorite_authors, fiction_or_nonfiction))
        
        conn.commit()
        conn.close()

        flash("Survey completed! Your dashboard has been updated.")
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('survey.html')

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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get user data
    c.execute("SELECT first_name, last_name FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()

    # Check if the survey is completed
    c.execute("SELECT * FROM survey WHERE user_id = ?", (user_id,))
    survey_data = c.fetchone()
    
    conn.close()

    has_completed_survey = survey_data is not None  # True if survey exists, False otherwise

    return render_template('dashboard.html', user=user, has_completed_survey=has_completed_survey)

# display all books in database
@app.route('/books')
def all_books():
    # connect to books database (Books table)
    db = bk.db_connection()
    # query Books table to display info on books
    books = bk.query_table()

    # return render_template()
    # (put HTML link in parentheses above & books = books)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))  # Redirects to the home page

if __name__ == '__main__':
    app.run(debug=True)
