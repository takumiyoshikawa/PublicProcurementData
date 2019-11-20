# PublicProcurementData

国土交通省の各地方整備局が公開している入札者情報をパネルデータとしてcsv化するコードを公開しています.

## Overview 

- crawling.py : 各地方整備局が公開しているhtmlファイルをクローリングするためのコードです.
- cleaning_.py : クローリングしたhtmlファイルを整形してcsvファイル形式で出力するためのコードです.
- util.py : 上記の二つのコードを実行するために必要な関数が保存されたファイルです.

## Data description

- 有資格者名簿の説明（データの内容 / 更新頻度など）
- civil engineering / consultingの説明
- なんかあれば

## Requirement
- crawling.py：Python3（動作確認環境:macOS catalina, Python 3.7.0）Pythonは[ここ](https://www.anaconda.com/distribution/)からインストールできます。また、crawling.pyを実行するには`python-Scrapy`が必要です。以下のコマンドでインストールできます。

```bash
pip install scrapy
```

## Usage

### crawling.py

1. `pip install scrapy`を実行して`python-Scrapy`をインストールしてください.
2. Rootpath, 地方整備局の有資格者名簿ホームのurl, 出力先のパスを設定してください.その際, 保存先のパスを
```bash
Rootpath/business_category/YYYYMMDD/~~~.html

ここに__main__を持ってきて説明をつける.不要な関数は全部utilにおいて短くする.
```
3. コマンドラインで`crawling.py`を実行してください.



### cleaning.py

1. クローリングしたデータを保存しているditrctory, 出力するcsvを保存するdirectoryをを指定してください.
```bash
if __name__ == "__main__":
    
    directory = 'directory/my_csv_panel.csv'
    file_list = list_all_files('Rootpath/region/bussiness_category/'
        , extension= 'html', sort = True)
    make_csv(file_list, directory)
```
2. コマンドラインで`cleaning.py`を実行してください.

## Remark
- cleaning.pyの指定先をbusiness_categoryレベルまで指定:当該bussiness_categoryのパネルデータを生成
- cleaning.pyの指定先をdateレベルまで指定:当該bussiness_categoryのクロスセクションデータを生成
```bash
if __name__ == "__main__":
    
    directory = 'directory/my_csv_cross_zsection.csv'
    file_list = list_all_files('Rootpath/region/bussiness_category/YYYYMMDD'
        , extension= 'html', sort = True)
    make_csv(file_list, directory)
```