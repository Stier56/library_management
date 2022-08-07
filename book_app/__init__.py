from datetime import timedelta
import os
from flask import Flask
from book_app.book_view import frontend
from book_app.database import create_table

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, instance_path=os.getenv('FLASK_INSTANCE_PATH'))
    # 設定ファイルの読み込み
    app.config.from_pyfile(os.getenv('FLASK_CONFIG'), silent=True)

    # dbオブジェクトのインポート
    dir_list = os.listdir("./")
    if "book.db" not in dir_list:
        with app.app_context():
            create_table()
        
    # blueprintで管理するサイトのurlを指定
    app.register_blueprint(frontend)

    return app