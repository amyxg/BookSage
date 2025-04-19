import sqlite3 as db
# from flask import g     # need to import flask in this file?

# Connects to Books Database

def db_connection():
    '''
    Function establishes a connection to database
    '''
    try:
        # establish a Connection to a SQLite file, indicating the filename
        connection = db.connect('books.db')
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
        cursor.execute('SELECT ISBN, Title, PubDate, Genre FROM Books')

        
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