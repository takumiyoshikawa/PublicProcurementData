# PublicProcurementData

国土交通省の各地方整備局が実施している入札の有資格業者名簿をパネルデータとしてcsv化するコードを公開しています.

## Overview 

- crawling.py : 各地方整備局が公開しているhtmlファイルをクローリングするためのコードです.
- cleaning_.py : クローリングしたhtmlファイルを整形してcsvファイル形式で出力するためのコードです.
- util.py : 上記の二つのコードを実行するために必要な関数が保存されたファイルです.

## Data description

- 有資格者名簿の説明（データの内容 / 更新頻度など）
- 有資格者名簿は, 各地方整備局が実施している入札に, 参加することができる事業者のリストを公開しています.
- 地方整備局に異なるが1月に1回から2回更新されています.　北海道開発局では月に1回, 東北, 関東, 中部, 近畿, 中国, 九州地方整備局では月に2回.
- 各地方整備局は建設工事やコンサルタント業務など20強の区分について, 入札に参加資格のある事業者の名義, 代表者氏名,　法人所在地, 法人番号, 技術評価点, 財務評価点を公開しています.   
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
2. 保存先のdirectoryをRootpathに, 取得したい地方整備局の有資格者名簿のurlをindex_urlに, 以下のように設定してください.
```bash
class Kanto_Spider(CrawlSpider):
    name = "kanto"
    index_url = "http://www.ktr.mlit.go.jp/honkyoku/nyuusatu/shikakushinsa/files/"
    Rootpath = '/Rootpath/kanto/'

    URL_List = URL_List(index_url)
    start_urls = URL_List.find_all_data_url()
    date_object = URL_list.get_update_date()

    path = pathlib.PosixPath(Rootpath + date_object)
    pathlib.Path.mkdir(path, exist_ok= True)

    def parse(self, response):
        filename = path + '/' + name + date_object + '_' + response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)
```
3. コマンドラインで以下により, `crawling.py`を実行してください.
```bash
scrapy crawl spider_name
```



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