# Book Database Data Dictionary

## Overview
This database appears to be designed for a book recommendation system that stores information about books, authors, users, and survey responses related to reading preferences.

## Tables

### Author
Stores information about book authors.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| AuthorID | INTEGER | Primary Key | Unique identifier for each author |
| Lastname | TEXT | | Author's last name |
| Firstname | TEXT | | Author's first name |

### Books
Stores information about books in the system.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| ISBN | INTEGER | Primary Key | International Standard Book Number, unique identifier for each book |
| Title | TEXT | NOT NULL | Book title |
| Pubdate | TEXT | | Publication date of the book |
| Genre | TEXT | NOT NULL | Primary genre of the book |
| Fiction_Nonfiction | TEXT | | Indicates if the book is fiction or non-fiction |
| Theme | TEXT | | Major theme or subject matter of the book |
| Tone | TEXT | | Emotional tone or mood of the book |
| Book_Length | TEXT | | Length category of the book (e.g., short, medium, long) |
| Book_Era | TEXT | | Historical period or era the book was written in or about |
| Narrative_Perspective | TEXT | | Point of view used in the narrative (e.g., first person, third person) |
| Book_Preference | TEXT | | Additional preference categorization |
| Description | TEXT | | Description of book |

### BookAuthor
Junction table that establishes a many-to-many relationship between books and authors.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| ISBN | INTEGER | Foreign Key (Books.ISBN) | Reference to a book's ISBN |
| AuthorID | INTEGER | Primary Key, Foreign Key (Author.AuthorID), AUTOINCREMENT | Reference to an author's ID |

### users
Stores information about system users.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| id | INTEGER | Primary Key, AUTOINCREMENT | Unique identifier for each user |
| first_name | TEXT | NOT NULL | User's first name |
| last_name | TEXT | NOT NULL | User's last name |
| email | TEXT | NOT NULL, UNIQUE | User's email address (must be unique) |
| password | TEXT | NOT NULL | User's encrypted password |
| has_completed_survey | INTEGER | DEFAULT 0 | Flag indicating whether the user has completed the reading preference survey (0=No, 1=Yes) |

### survey_responses
Stores users' responses to the reading preference survey.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| id | INTEGER | Primary Key, AUTOINCREMENT | Unique identifier for each survey response |
| user_id | INTEGER | NOT NULL, Foreign Key (users.id) | Reference to the user who submitted the response |
| reading_frequency | TEXT | | How often the user reads |
| book_preference | TEXT | | General book preferences |
| discover_method | TEXT | | How the user typically discovers new books |
| genres | TEXT | | Preferred genres |
| fiction_non_fiction | TEXT | | Preference for fiction or non-fiction |
| explore_genres | TEXT | | Genres the user would like to explore |
| tone | TEXT | | Preferred emotional tone in books |
| themes | TEXT | | Preferred themes or subject matters |
| book_length | TEXT | | Preferred book length |
| book_era | TEXT | | Preferred historical era or time period |
| narrative_perspective | TEXT | | Preferred narrative perspective |
| favorite_authors | TEXT | | User's favorite authors |
| top_books | TEXT | | User's top books |
| reading_purpose | TEXT | | User's primary purpose for reading |
| thought_provoking | TEXT | | Whether the user prefers thought-provoking content |

### sqlite_sequence
System table used by SQLite to keep track of the last used AUTOINCREMENT value for each table.

| Column | Data Type | Description |
|--------|-----------|-------------|
| name | TEXT | Name of the table that uses AUTOINCREMENT |
| seq | INTEGER | Last used sequence number |

## Entity Relationships

1. **Books to Authors** (Many-to-Many):
   - A book can have multiple authors
   - An author can write multiple books
   - The BookAuthor table facilitates this relationship

2. **Users to Survey Responses** (One-to-One):
   - Each user can have one survey response
   - Each survey response belongs to one user
   - The has_completed_survey field in users table tracks if a user has submitted a response

## Database Schema Diagram

```
Author 1──┐
          │
          │ BookAuthor
          │
Books 1───┘
          
users 1─────1 survey_responses
```

## Notes
- The system appears designed to collect user reading preferences through a survey and potentially offer book recommendations based on these preferences.
- The Books table contains detailed information about books including metadata like genre, tone, theme, and narrative style.
- User authentication is handled through the users table with email and password fields.
