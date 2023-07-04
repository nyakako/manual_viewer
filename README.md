## ローカル実行環境の設定方法

今回のインターン課題はdjango 4.2で開発しています。

python バージョン3.8以降の環境で下記の手順をお願いいたします。

https://docs.djangoproject.com/ja/4.2/faq/install/#faq-python-version-support

※開発環境はPython 3.10.9です。


### 1. お好みのディレクトリでgit cloneします。

`git clone git@jpt-intern-gitlab.eastus.cloudapp.azure.com:nakamura-group/manual_viewer_win.git`



### 2. 次にcloneしたディレクトリに移動して、仮想環境を作成、起動します。

`cd manual_viewer_win`

`python -m venv [仮想環境名]`

`source [仮想環境名]\bin\activate`



### 3. 次に仮想環境に必要なライブラリをpip installします。

`pip install -r requirements.txt`



### 4. プロジェクトフォルダに移動します。

`cd manualproject`



### 5. 次にsuperuserを作成してください。

`python manage.py createsuperuser`



### 6. ローカルサーバーを起動して動作確認をお願いいたします。

`python manage.py runserver`



### ■備考

今回、動作確認用にソースコード内にサンプルデータとしてdb.sqlite3、mediaフォルダ、staticフォルダを含めたのでmigrateは不要です。

（※通常dbやmedia、staticフォルダはソースに含まないことは理解しておりますが、今回は動作確認をスムーズにして頂くために含めました。ローカル環境でdebug =falseにする為、setting.pyの設定も一部通常デプロイする場合とは異なる特殊な設定となっています。）
