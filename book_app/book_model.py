import csv
from flask import current_app
import requests
from book_app.book import Book
from book_app.database import get_db


def search_book_from_db(title, author):
    con = get_db()
    cur = con.cursor()
    try:
        sql = "SELECT * FROM books WHERE title LIKE \"%{}%\" AND author LIKE \"%{}%\";".format(title, author)
        cur.execute(sql)
        records = cur.fetchall()

        books = []
        for record in records:
            book = Book(record[1], record[2], record[0], record[3], record[4], record[5], record[6])
            books.append(book)
    except:
        print("error occurred")
    finally:
        cur.close()
        con.close()

    return books


def get_book_from_db(isbn):
    book=None
    con = get_db()
    cur = con.cursor()
    try:
        sql = "SELECT * FROM books WHERE isbn={};".format(isbn)
        cur.execute(sql)
        records = cur.fetchall()
        record = records[0]
        book = Book(record[1], record[2], record[0], record[3], record[4], record[5], record[6])
    except:
        print("error occurred")
    finally:
        cur.close()
        con.close()

    return book


def insert_book_to_db(book):
    flag = False
    con = get_db()
    cur = con.cursor()
    try:
        sql = "INSERT INTO books(title, author, isbn, publisher, storage, description, thumbnail) \
            VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(book.title, book.author, book.isbn, book.publisher, book.storage, book.description, book.thumbnail)
        cur.execute(sql)
        con.commit()
        flag = True
    except:
        con.rollback()
        print("error occurred")
    finally:
        cur.close()
        con.close()

    return flag


def add_book_from_csv(file_path):
    with open(file_path) as f:
        csv_reader = csv.reader(f)

        count = 0
        con = get_db()
        cur = con.cursor()
        for book in csv_reader:
            title = book[0]
            author = book[1]
            isbn = book[2]
            isbn = isbn.replace('-','')
            publisher = book[3]
            storage = book[4]

            book = get_bookinfo_from_api(isbn)

            try:
                sql = "INSERT INTO books(title, author, isbn, publisher, storage, description, thumbnail) \
                VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(title, author, isbn, publisher, storage, book.description, book.thumbnail)
                cur.execute(sql)
                con.commit()
                count = count + 1
            except:
                con.rollback()
                print("error occurred")
            
        cur.close()
        con.close()

    return count

        
def delete_book_from_db(isbn):
    flag = False
    con = get_db()
    cur = con.cursor()
    try:
        sql ="DELETE FROM books WHERE isbn={};".format(isbn)
        cur.execute(sql)
        con.commit()
        flag = True
    except:
        con.rollback()
        print("error occurred")
    finally:
        cur.close()
        con.close()

    return flag


def modify_book(book):
    flag = False
    con = get_db()
    cur = con.cursor()    
    try:
        sql = "UPDATE books SET title='{}', author='{}', publisher='{}', storage='{}', description='{}' \
            WHERE isbn={};".format(book.title, book.author, book.publisher, book.storage, book.description, book.isbn)    
        cur.execute(sql)
        con.commit()
        flag = True
    except:
        con.rollback()
        print("error occurred")
    finally:
        cur.close()
        con.close()

    return flag

def get_bookinfo_from_api(book_isbn):
    api_url = current_app.config['API_URL']
    api_key = current_app.config['API_KEY']
    req_url = api_url + book_isbn + '&key=' + api_key
    no_image_path = current_app.config['NO_IMAGE']

    try:
        api_response = requests.get(req_url, timeout=3.0)
    except:
        print("request timeout")

    book = Book()
    book.isbn = book_isbn
    if api_response.status_code == 200:
        json_data = api_response.json()
        if 'items' in json_data:
            book_data = json_data.get('items')[0].get('volumeInfo')
            # タイトル
            book.title = book_data.get('title', 'NoData')
            # 著者
            book.author = book_data.get('authors', 'NoData')
            if book.author != 'NoData':
                book.author = ','.join(book_data.get('authors'))
            # 出版社
            book.publisher = book_data.get('publisher', 'NoData')
            # 説明
            book.description = book_data.get('description', 'NoData')
            # サムネイル
            book.thumbnail = book_data.get('imageLinks', no_image_path)
            if book.thumbnail != no_image_path:
                book.thumbnail = book_data.get('imageLinks').get('thumbnail', no_image_path)

    return book


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS