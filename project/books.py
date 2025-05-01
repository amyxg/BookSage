import sqlite3 as db
# from flask import flask, g     # need to import flask in this file?

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
    Function queries a database
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
        Books.Fiction_Nonfiction,
        Books.Theme,
        Books.Tone,
        Books.Book_Length,
        Books.Book_Era,
        Books.Narrative_Perspective,
        Books.Book_Preference,
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

        print(results)      # can comment out, this just shows results are  
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
    
# call functions   
conn = db_connection()
query_table(conn)