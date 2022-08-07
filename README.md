# library_management
蔵書の管理をするために作成したwebアプリケーション。  
webアプリの勉強を兼ねて作成しました。  
※個人的に使用する目的で作成したものなので、使用する際は自己責任でお願い致します。

## Useage
1. ``instance``内の設定ファイルの編集  

|変数名  |内容  |
|:---:|:---:|
|DATABASE     | 使用するデータベース名  |
|API_URL  |　使用するAPIのURL（今回はgoogle books apiを使用）  |
|UPLOAD_FOLDER        |　csvファイルから書籍データを読み込む際に使用するcsvファイルの一時保管場所  |
|NO_IMAGE       |　APIから書影を得られなかった際に使用する画像  |


2. 環境変数の設定
```
export FLASK_APP=book_app
export FLASK_INSTANCE_PATH='/your/instance/absolute/directory/path/'
export FLASK_CONFIG='sample.cfg'
```
3. 実行  
``flask run``

