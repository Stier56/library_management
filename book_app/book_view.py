import os
from flask import Blueprint, current_app, flash, render_template, request
from sqlalchemy import null
from book_app.book import Book
from book_app import book_model
from werkzeug.utils import secure_filename

frontend = Blueprint('book-management', __name__, url_prefix='/book-management', template_folder='templates', static_folder='static')


@frontend.route('/menu', methods=['GET'])
def menu():
    return render_template('menu.html')


@frontend.route('/search', methods=['POST'])
def search():
    book_title = request.form.get("title")
    book_author = request.form.get("author")
    books = book_model.search_book_from_db(book_title, book_author)

    return render_template('search.html', books=books)


@frontend.route('/add', methods=['GET', 'POST'])
def add():
    # GETメソッド時の処理
    if request.method == 'GET':
        return render_template('add.html', book=None) 
    # POSTメソッド時の処理
    else:
        if request.form.get('search_button') == 'search_book':
            book_isbn = request.form.get("isbn")
            # api問い合わせ
            book = book_model.get_bookinfo_from_api(book_isbn)
            
            return render_template('add.html', book=book)
        else:
            book = Book(request.form.get("title"),
                        request.form.get("author"),
                        request.form.get("isbn"),
                        request.form.get("publisher"),
                        request.form.get("storage"),
                        request.form.get("description"),
                        request.form.get("thumbnail"))

            flag = book_model.insert_book_to_db(book)

            if flag is True:
                return render_template('add.html', book=None)
            else:
                flash('エラーが発生しました。書籍はすでに登録されている可能性があります。')
                return render_template('menu.html')


@frontend.route('/add-csv', methods=['POST'])
def add_from_csv():
    if 'csv' not in request.files:
        flash('ファイルが選択されていません')
        return render_template('add.html', book=None)

    file = request.files['csv']

    if file.filename == '':
        flash('ファイルが選択されていません。')
        return render_template('add.html', book=None)

    if file and book_model.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        count = book_model.add_book_from_csv(file_path)

        os.remove(file_path)
        flash('{}冊の書籍情報の追加が完了しました。'.format(count))
        return render_template('add.html', book=null)
    else:
        flash('CSVファイルからの書籍の追加に失敗しました。')
        return render_template('add.html', book=None)


@frontend.route('/delete', methods=['POST'])
def delete():
    book_isbn = request.form.get("delete_book")
    book = book_model.get_book_from_db(book_isbn)

    return render_template('delete.html', book=book)


@frontend.route('/delete-complete', methods=['POST'])
def delete_complete():
    book_isbn = request.form.get("delete_book")
    flag = book_model.delete_book_from_db(book_isbn)

    if flag is True:
        return render_template('menu.html')
    else:
        flash('エラーが発生しました。書籍情報を削除できませんでした。')
        return render_template('menu.html')


@frontend.route('/modify', methods=['POST'])
def modify():
    book_isbn = request.form.get("modify_book")
    book = book_model.get_book_from_db(book_isbn)

    return render_template('modify.html', book=book)


@frontend.route('/modify-complete', methods=['POST'])
def modify_complete():
    book = Book(request.form.get("title"), 
                request.form.get("author"),
                request.form.get("isbn"),
                request.form.get("publisher"),
                request.form.get("storage"),
                request.form.get("description"),
                request.form.get("thumbnail"))

    flag = book_model.modify_book(book)

    if flag is True:
        return render_template('menu.html')
    else:
        flash('エラーが発生しました。書籍情報を更新できませんでした。')
        return render_template('menu.html')
    







