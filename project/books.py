import sqlite3 as db

# Connects to Books Database

def db_connection():
    '''
    Function establishes a connection to database
    '''
    try:
        # establish a Connection to a SQLite file, indicating the filename
        connection = db.connect('books.db')
    except Exception as e:
        print(e)

def query_table(connection):
    '''
    Function queries a database
    '''
    try:
        #cursor used to submit DB requests/get results
        cursor = conn.cursor()
        
        # execute SQL command to get books
        cursor.execute('SELECT ISBN, Title, PubDate, Genre FROM Books')

        
        # get results
        rows = cursor.fetchall()
        
        #print header rows
        for fieldinfo in cursor.description:
            print(fieldinfo[0], end="|")
        print()
        
        for row in rows:
            print(row)
        
        
    # exception handling errors
    except Exception as e:
        print(e)
        
    # end function by closing connection
    finally:
        cursor.close()
        conn.close()
    
# call functions   
conn = db_connection()
query_table(conn)