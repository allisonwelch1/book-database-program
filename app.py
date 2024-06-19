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
    add_csv()
    app()

    for book in session.query(Book):
        print(book)
