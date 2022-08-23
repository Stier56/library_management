# library_management
蔵書の管理をするために作成したwebアプリケーション。  
webアプリの勉強を兼ねて作成しました。  
※個人的に使用する目的で作成したものなので、使用する際は自己責任でお願い致します。

## Useage
1. 自身の環境にflaskとrequestsをインストール

2. ``instance/``内の設定ファイルを自身の環境に合わせて編集  

|変数名  |内容  |
|:---:|:---:|
|DATABASE             | 使用するデータベース名  |
|API_URL              |　使用するAPIのURL（今回はgoogle books apiを使用）  |
|API_KEY              |　使用するAPIのKEY  |
|SESSION_SECRET_KEY   |  セッションを暗号化するKEY |
|UPLOAD_FOLDER        |　csvファイルから書籍データを読み込む際に使用するcsvファイルの一時保管場所  |

3. run_app.shを自身の環境に合わせて編集
```
export FLASK_APP=book_app
export FLASK_INSTANCE_PATH='/your/instance/absolute/directory/path/'
export FLASK_CONFIG='sample.cfg'
flask run
```
4. run_app.shの実行  

