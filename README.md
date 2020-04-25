# 公共調達のデータ整備

このrepositoryでは、国土交通省の各地方整備局が実施している公共調達の経済学分析に役立つデータとその収集・整理のためのコードを公開している。各地方整備局は、競争入札によって、土木工事や測量事業などを調達している。まず、その入札のデータを公開している。また、この競争入札に参加するためには競争参加資格を得る必要があり、各地方整備局が随時申請を受け付けている。この有資格者名簿のデータを、収集するためのコードとともに公開している。

## 1. データ

公開しているデータは、入札データと有資格者名簿データである。

### 1.1. 入札データ

予定価格が一定額を超える中大規模の一般競争入札（オークションによる調達）において、どの企業がいくらで入札し評価値 (入札額および品質によりつけられた値 ) がいくらであったか、およびどの企業が落札したかというデータを掲載している。原則として 最新 2年度分のデータが csv形式で各地方整備局のHPに掲載されて、ここでは2018年度と2019年度のデータを公開している。

### 1.2. 有資格者名簿データ

各事業に入札を行うためには資格が必要となり、各地方整備局が随時申請を受け付けている . 有資格者名簿は各自治体のホームページに html形式で掲載されている。資格は２年間有効で、1月毎に有資格者の一覧は更新され、過去の情報は削除される 。 一ヶ月毎にクローリングすることで参入のデータを整理している。

事業には、主に建設工事とコンサルティングがある。例えば、建設工事には土木や鋼橋などがあり、コンサルティング業務には測量や地質調査などがある。名簿は一ヶ月に1回から2回更新されており、建設工事については2019年9月から、コンサルティング業務については2019年12月からデータを集めている。なお、更新頻度は以下のように地方によって異なる。

- 月1回…北海道開発局
- 月2回…東北, 関東, 中部, 近畿, 中国, 九州地方整備局

#### 建設工事事業の変数

まず、有資格者の基礎変数とデータの更新日時がある。

| 基礎変数名   | 意味             |
| :----------- | ---------------- |
| firm_name    | 商号又は名称     |
| ceo_name     | 代表者名         |
| firm_address | 住所             |
| firm_id      | 法人番号         |
| date         | データの更新日時 |

- なお、Joint Ventureの場合は`JV`が入力され, 法人番号のない企業には何も入力されていない。

そして、資格の内容を表す変数名は、事業内容と評価内容を組み合わせてできている。例えば、civilengineering_qualificationとは、「土木工事の等級」という意味である。

| 事業内容         | 意味               |
| :--------------- | ------------------ |
| civilengineering | 一般土木           |
| asphalt          | アスファルト       |
| bridge           | 鋼橋上部           |
| landscaping      | 造園               |
| building         | 建築               |
| woodenbuilding   | 木造建築           |
| electricity      | 電気設備           |
| airconditioning  | 暖冷房衛生設備     |
| cement           | セメント           |
| prestressed      | プレストレスメント |
| slope            | 法面処理           |
| painting         | 塗装               |
| maintenance      | 維持修繕           |
| dredging         | しゅんせつ         |
| grout            | グラウト           |
| stakeout         | 杭打               |
| well             | さく井             |
| prefab           | プレハブ建築       |
| machinery        | 機械設備           |
| communication    | 通信設備           |
| substation       | 受変電設備         |

| 評価内容        | 意味           |
| :-------------- | -------------- |
| qualification   | 等級           |
| rank            | 順位           |
| exception       | 例外処理用の欄 |
| financial_score | 経審評価点数   |
| technical_score | 技術評価点数   |
| total_score     | 総合点数       |

なお北海道に限っては事業内容の変数構成が異なる。

| 事業内容         | 意味               |
| :--------------- | ------------------ |
| civilengineering | 一般土木          |
| building         | 建築               |
| asphalt          | 舗装　　　　      |
| bridge           | 鋼橋上部           |
| prestressed      | PSコンクリート    |
| dredging         | しゅんせつ         |
| machinery        | 機械装置           |
| pipe             | 管              |
| electricity      | 電気            |
| painting         | 塗装               |
| landscaping      | 造園               |
| waterproof       | 防水加工         |
| well             | さく井             |
| grout            | グラウト           |
| maintenance      | 維持             |
| others           | その他           |



#### コンサルティング事業の変数

コンサルティング事業における変数は以下である。

| 基礎変数名   | 意味             |
| :----------- | ---------------- |
| firm_name    | 商号又は名称     |
| firm_id      | 法人番号         |
| prefecture   | 所在県名         |
| firm_size    | 規模           | 
| date         | データの更新日時 |
| building_consulting | 建築関係コンサルティングの順位 |
| civilengineering_consulting | 土木関係コンサルティングの順位 |
| geological_survey | 地質調査の順位 |
| compensation_consultant | 補償関係コンサルタントの順位 |




## 2. コード(有資格業者名簿)

有資格業者名簿のデータを活用する際、どのようにしてデータが編集されたのかを知ることが役に立つ。そこで、ここではデータ収集および編集のコードを公開する。

### 2.1. コード内容

データ収集と編集のためのコードは以下3つの.pyファイルにまとめられている。

1. crawling.py … 各地方整備局が公開しているhtmlファイルをクローリングするためのコード
2. cleaning.py … クローリングしたhtmlファイルを整形してcsvファイル形式で出力するためのコード(各地方ごとのコードをまとめてある)

Python3（動作確認環境:macOS catalina, Python 3.7.0）Pythonは[ここ](https://www.anaconda.com/distribution/)からインストールできる。crawling.pyを実行するには`python-Scrapy`が必要であり、以下のコマンドでインストールできる：

```bash
pip install scrapy
```

### 2.2. 手順


以下の手順で、上記の.pyファイルを実行してデータを収集している.

#### crawling.py

1. `pip install scrapy`を実行して`python-Scrapy`をインストールする
2. 保存先のdirectoryをRootpathに, 取得したい地方整備局の有資格者名簿のurlをindex_urlに, 以下のように設定する

- 以下では関東地方整備局をクローリングする例
```bash
class Kanto_Spider(CrawlSpider):
    name = "kanto"

    def __init__(self, category=None, *args, **kwargs):
        super(Kanto_Spider, self).__init__(*args, **kwargs)
        
        // 年度の変更によってindex_url変更の可能性あり.
        self.index_url = 'http://www.ktr.mlit.go.jp/honkyoku/nyuusatu/shikakushinsa/files/'　
        self.Rootpath = './data/kanto/'
        
        self.URL_List = URL_List(self.index_url, self.Rootpath)
        self.start_urls = self.URL_List.find_all_data_url()
        self.date_object = self.URL_List.get_update_date()
        self.URL_List.make_directory()


    def parse(self, response):
        html_name = response.url.split('/')[-1]

        // 各整備局のアップローディングルールにより, 30未満は工事区分 30以上はコンサルティング区分
        if int(re.search('\d+', html_name).group()) < 30:
            filename = self.Rootpath + 'civil_engineering/' + self.date_object + '/' + self.name + '_' + self.date_object + '_' + response.url.split("/")[-1]
        else:
            filename = self.Rootpath + 'consulting/' + self.date_object + '/' + self.name + '_' + self.date_object + '_' + response.url.split("/")[-1]
        
        with open(filename, 'wb') as f:
            f.write(response.body)

```

3. コマンドラインで以下により, `crawling.py`を実行する.ここでは例として, `name`は`kanto`になる

```bash
scrapy crawl name
```

#### cleaning.py

0. このコードは `./region/business_category/date/` というディレクトリ構造に従ってデータを保存していることに依拠している。
```
.
├── code
│   └── cleaning.py
└── data
    ├── chubu
    │   ├── construction
    │   │   ├── 20191001
    │   │   │   ├── chubu_20191001_eq_saku17YDn.html
    │   │   │   ├── chubu_20191001_eq_saku17YDr.html
    │   │   │   └── chubu_20191001_eq_saku17YDs.html
    │   │   └── 20191015
    │   └── consulting
    ├── chugoku
    ├── hokkaido
    ├── kanto
    ├── kinki
    └── kyushu
```

1. クローリングしたデータを保存しているditrctory, 出力するcsvを保存するdirectoryをを指定する。

- `region`には指定したい地域、例えば`chubu`を記述する。
- `business_category`には指定したい業態、例えば`construction`を記述する。
- `date`には指定したい日付、例えば`20191001`を記述する。

```bash
if __name__ == "__main__":
    
    output = '../region/output/business_category/region_business_category_date.csv'
    file_list = list_all_files('./data/region/business_category/date'
        , extension= 'html', sort = True)
    make_csv(file_list, output)
```

2. コマンドラインで`cleaning.py`を実行する.

### 2.3. ライセンス

Unlicenseに即し、全てのデータ、コードおよびドキュメントはパブリックドメインである。

