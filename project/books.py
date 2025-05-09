import sqlite3 as db

# Connects to Books Database

def db_connection():
    '''
    Function establishes a connection to database
    '''
    try:
        # establish a Connection to a SQLite file, indicating the filename
        connection = db.connect('bookSage.db')
        # set the row factory to return dictionary objects
        connection.row_factory = db.Row

        return connection

    except Exception as e:
        print(e)

def query_table(connection):
    '''
    Function queries a database to show all books 
    and their respective Author's First & Last Name,
    ISBN, Title, Publication Date & Genre.

    '''
    try:
        #cursor used to submit DB requests/get results
        cursor = connection.cursor()
        
        # execute SQL command to get books
        cursor.execute('''
    SELECT 
        Books.ISBN,
        Books.Title,
        Books.PubDate,
        Books.Genre,
        Author.Firstname,
        Author.Lastname
    FROM 
        Books
    JOIN 
        BookAuthor ON Books.ISBN = BookAuthor.ISBN
    JOIN 
        Author ON BookAuthor.AuthorID = Author.AuthorID
''')
   
        # get results
        rows = cursor.fetchall()
        
        # convert rows to dictionaries
        results = [dict(row) for row in rows]

        # print(results)      # can comment out, this just shows results are  
                            # in a list of dictionaries

        return results
        
        
    # exception handling errors
    except Exception as e:
        print(e)
        return []       # empty list
        
    # end function by closing connection
    finally:
        cursor.close()
        connection.close()

def get_book_by_isbn(connection, isbn):
    """
    Fetches individual book details by ISBN, including author, 
    description, etc.
    """
    try:
        #cursor used to submit DB requests/get results
        cursor = connection.cursor()
        cursor.execute('''
            SELECT 
                Books.ISBN,
                Books.Title,
                Books.PubDate,
                Books.Genre,
                Books.Fiction_Nonfiction,
                Books.Theme,
                Books.Tone,
                Books.Book_Length,
                Books.Book_Era,
                Books.Narrative_Perspective,
                Books.Book_Preference,
                Books.Description,
                Author.FirstName,
                Author.LastName
            FROM Books
            JOIN BookAuthor ON Books.ISBN = BookAuthor.ISBN
            JOIN Author ON BookAuthor.AuthorID = Author.AuthorID
            WHERE Books.ISBN = ?
        ''', (isbn,))

        # return one book at a time
        row = cursor.fetchone()

        # convert row to dictionaries
        return dict(row) if row else None

    # except handling errors, print error, return empty list
    except Exception as e:
        print(e)
        return []   # empty list

    # end function by closing connection & cursor
    finally:
        cursor.close()
        connection.close()

def get_user_by_id(user_id):
    conn = db.connect('bookSage.db')
    conn.row_factory = db.Row  # This lets you access rows as dicts
    cursor = conn.cursor()

    cursor.execute('''
        SELECT first_name, last_name, email
        FROM Users
        WHERE id = ?
    ''', (user_id,))
    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None


# call functions   
# conn = db_connection()
# query_table(conn)