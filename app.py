from models import (Base, session,
                    Book, engine)
import datetime
import csv
import time


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
    try:  # put desired code here
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:  # if it doesn't work,
        input('''
        \n********************DATE ERROR***********************
        \rThe date format should include a valid Month Day Year
        \rEx: October 14, 1997
        \rPress enter to try again
        \r*****************************************************''')
    else:
        return return_date


def clean_price(price_str):
    try:
        price_float = float(price_str)
        return_price = int(price_float * 100)
    except ValueError:
        input('''
        \n***********************PRICE ERROR*************************
        \rThe price format should include all dollar and cents values 
        \r(no currency symbols)
        \rEx: 14.99
        \rPress enter to try again
        \r************************************************************''')
    else:
        return return_price


def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
            \n********ID ERROR*********
            \rThe ID should be a number
            \rPress enter to try again
            \r**************************''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
                \n********ID ERROR*********
                \rOptions: {options}
                \rPress enter to try again
                \r**************************''')
            return



def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
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
            title = input('Title: ')
            author = input('Author: ')
            # need to handle errors associated w incorrect format of date and price
            # see type/except/else in clean_date() and clean_price()
            date_error = True
            while date_error:
                date = input('Published Date (Ex: October 25, 2017): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            # set a variable equal to True
            # while it's true, the app will continue to ask for the date
            # date_error being true is contingent on the fact that we're getting a ValueError
            # in clean_date
            # once we get a date that's formatted correctly (datetime.date),
            # date_error = False and move on
            price_error = True
            while price_error:
                price = input('Price (Ex: 25.00): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book added successfully.')
            time.sleep(2)  # in "time" module: delays app by 2 seconds so user can see message
        elif choice == '2':
            # view books
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\nPress enter to return to main menu.')
        elif choice == '3':
            # search book
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nID Options: {id_options}
                    \rBook id:  ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id==id_choice).first()
            print(f'''
                \n{the_book.title} by {the_book.author}
                \rPublished: {the_book.published_date}
                \rPrice: ${the_book.price / 100}''')
            input('\nPress enter to return to main menu.')
        elif choice == '4':
            # analysis
            pass
        else:
            print('GOODBYE')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
