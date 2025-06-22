import pymysql

# Connect to MySQL Server
try:
    con = pymysql.connect(host="localhost", user="root", password="your_password")
    cursor = con.cursor()

    # Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS LibraryDB")
    cursor.execute("USE LibraryDB")

    # Create books table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        available BOOLEAN DEFAULT TRUE
    )
    """)

    con.commit()
    print("Database and Table Setup Completed!")
except Exception as e:
    print("Error connecting to MySQL:", e)
    exit()

# Function to add a book
def add_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    cursor.execute("INSERT INTO books (title, author, available) VALUES (%s, %s, %s)", (title, author, True))
    con.commit()
    print("Book added successfully!")

# Function to view all books
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\nLibrary Books:")
    for book in books:
        status = "Available" if book[3] else "Borrowed"
        print(f"{book[0]}. {book[1]} by {book[2]} - {status}")
    print()

# Function to borrow a book
def borrow_book():
    view_books()
    book_id = input("Enter the Book ID to borrow: ")
    cursor.execute("UPDATE books SET available = FALSE WHERE id = %s AND available = TRUE", (book_id,))
    if cursor.rowcount > 0:
        con.commit()
        print("Book borrowed successfully!")
    else:
        print("This Book is not available!")

# Function to return a book
def return_book():
    book_id = input("Enter the Book ID to return: ")
    cursor.execute("UPDATE books SET available = TRUE WHERE id = %s AND available = FALSE", (book_id,))
    if cursor.rowcount > 0:
        con.commit()
        print("Book is returned successfully!")
    else:
        print("Invalid Book ID or book wasn't borrowed.")

# Main menu
while True:
    print("\nLibrary Management System")
    print("1. Add Book")
    print("2. View Books")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        borrow_book()
    elif choice == "4":
        return_book()
    elif choice == "5":
        print("Exiting! Thank you.")
        break
    else:
        print("Invalid choice! Try again.")

# Close the database connection
con.close()
