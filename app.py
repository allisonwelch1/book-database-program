from models import (Base, session,
                    Book, engine)
import datetime
import csv


def menu():
    while True:
        print('''
            \nPROGRAMMING BOOKS
            \r1) ADD BOOK
            \r2) VIEW ALL BOOKS
            \r3) SEARCH FOR BOOK
            \r4) BOOK ANALYSIS
            \r5) EXIT''')

        choice = input('What would you like to do? ')

        if choice in ('1', '2', '3', '4', '5'):
            return choice  # Valid choice, return it and exit the function
        else:
            input('''
            \rPlease choose one of the options above.
            \rA number from 1-5.
            \rPress enter to try again
            ''')  # Invalid choice, prompt the user and loop again
# add books to the database
# edit books
# delete books
# search books
# data cleaning


def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    split_date = date_str.split(' ')
    month = int(months.index(split_date[0]) + 1)
    day = int(split_date[1].split(',')[0])
    year = int(split_date[2])
    return datetime.date(year, month, day)


def clean_price(price_str):
    price_float = float(price_str)
    return int(price_float * 100)


def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            title = row[0]
            author = row[1]
            date = clean_date(row[2])
            price = clean_price(row[3])
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            # For each row in database it sets title, author, date, price, creates a new book,
            # and adds the new book to the session. Loops through all rows (all books)
        session.commit()  # Then commits all books outside loop


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # add book
            pass
        elif choice == '2':
            # view books
            pass
        elif choice == '3':
            # search book
            pass
        elif choice == '4':
            # analysis
            pass
        else:
            print('GOODBYE')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # app()
    add_csv()

    for book in session.query(Book):
        print(book)
