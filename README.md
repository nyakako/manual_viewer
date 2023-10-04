## ローカル実行環境の設定方法

このアプリケーションは django 4.2 で開発しています。

python バージョン 3.8 以降の環境で下記の手順をお願いいたします。

https://docs.djangoproject.com/ja/4.2/faq/install/#faq-python-version-support

※開発環境は Python 3.10.9 です。

### 1. お好みのディレクトリで git clone します。

`git clone https://github.com/nyakako/manual_viewer.git`

### 2. 次に clone したディレクトリに移動して、仮想環境を作成、起動します。

`cd manual_viewer`

`python -m venv [仮想環境名]`

`source [仮想環境名]\bin\activate`

### 3. 次に仮想環境に必要なライブラリを pip install します。

`pip install -r requirements.txt`

### 4. プロジェクトフォルダに移動します。

`cd manualproject`

### 5. 次に superuser を作成してください。

`python manage.py createsuperuser`

### 6. ローカルサーバーを起動して動作確認をお願いいたします。

`python manage.py runserver`

### ■ 備考

今回、動作確認用にソースコード内にサンプルデータとして db.sqlite3、media フォルダ、static フォルダを含めたので migrate は不要です。

（※通常 db や media、static フォルダはソースに含まないことは理解しておりますが、今回は動作確認をスムーズにして頂くために含めました。ローカル環境で debug =false にする為、setting.py の設定も一部通常デプロイする場合とは異なる特殊な設定となっています。）
