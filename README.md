# PublicProcurementData

国土交通省の各地方整備局が実施している競争入札の有資格業者名簿をcsvデータとして公開しています.

## Overview

- 国土交通省の地方整備局は, 土木工事や測量事業等を競争入札によって受注しています.
- 競争入札に参加するためには競争参加資格を得る必要があり, 各地方整備局が随時申請を受け付けています. 
	- 参照 : 中部地方整備局の例 (https://www.cbr.mlit.go.jp/contract/kyousou/index.htm)
- 各地方整備局は, 競争参加資格を持つ企業のリストを有資格者名簿として公開しています.
- 本プロジェクトでは, html形式でデータを公開している, 北海道地方開発局, 東北地方整備局, 関東地方整備局, 中部地方整備局, 近畿地方整備局, 中国地方整備局, 九州地方整備局について, 有資格者名簿をcsv形式でパネルデータ化することを目的としています.

## Data description

- 有資格者名簿は, 各地方整備局が実施している入札に, 参加することができる事業者のリストのことです.
- 地方整備局によって異なりますが一ヶ月に1回から2回更新されています.　北海道開発局では月に1回, 東北, 関東, 中部, 近畿, 中国, 九州地方整備局では月に2回の更新です.
- 各地方整備局は建設工事やコンサルタント業務など20強の区分について, 入札に参加資格のある事業者の名義, 代表者氏名,　法人所在地, 法人番号, 技術評価点, 財務評価点, 総合評価点等を公開しています.   
- 事業は土木, 鋼橋といった建設工事と, 測量や地質調査などのコンサルティング業務があります. 

関東地方整備局を例にとって, データの中身を説明します.
- 建設工事
	- firm_name : 商号又は名称
	- ceo_name : 代表者名
	- firm_address : 住所
	- firm_id : 法人番号
		- Joint Ventureの場合は`JV`が入力され, 法人番号のない企業には何も入力されていません.
	- civilengineering_{qualification/rank/exception/financial_score/technical_score/total_score} : 土木工事の{等級/順位/例外処理用の欄/経審評価点数/技術評価点数/総合点数}
	- asphalt_{同上} : アスファルトの{同上}
	- bridge_{同上} : 鋼橋上部の{同上}
	- landscaping_{同上} : 造園の_{同上}
	- builiding_{同上} : 建築の{同上}
	- woodenbuiliding_{同上} : 木造建築の{同上}
	- electricity_{同上} : 電気設備_{同上}
	- airconditioning_{同上} : 暖冷房衛生設備の{同上}
	- cement_{同上} : セメントの{同上}
	- prestressed_{同上} : プレストレスメントの_{同上}
	- slope_{同上} : 法面処理の{同上}
	- painting_{同上} : 塗装の{同上}
	- maintenance_{同上} : 維持修繕の_{同上}
	- dredging_{同上} : しゅんせつの{同上}
	- grout_{同上} : グラウトの{同上}
	- stakeout_{同上} : 杭打の_{同上}
	- well_{同上} : さく井の{同上}
	- prefab_{同上} : プレハブ建築の{同上}
	- machinery_{同上} : 機械設備の_{同上}
	- communication_{同上} : 通信設備の{同上}
	- substation_{同上} : 受変電設備の{同上}
	- date : データの更新日時
- コンサルタント業務
	- firm_name : 商号又は名称
	- firm_id : 法人番号
	- prefecture : 所在県名
	- firm_size : 規模
	- surveying : 測量の順位
	- building_consulting : 建築関係コンサルティングの順位
	- civilengineering_consulting : 土木関係コンサルティングの順位
	- geological_survey : 地質調査の順位
	- compensation_consultant : 補償関係コンサルタントの順位

- 各業種への参加資格を保有しない場合, 当該業種に関連する変数は欠損値になっています. 

## License
<!--
## Overview 

- crawling.py : 各地方整備局が公開しているhtmlファイルをクローリングするためのコードです.
- cleaning_.py : クローリングしたhtmlファイルを整形してcsvファイル形式で出力するためのコードです.
- util.py : 上記の二つのコードを実行するために必要な関数が保存されたファイルです.

## Data description

- 有資格者名簿の説明（データの内容 / 更新頻度など）
- 有資格者名簿は, 各地方整備局が実施している入札に, 参加することができる事業者のリストのことです.
- 地方整備局によって異なりますが一ヶ月に1回から2回更新されています.　北海道開発局では月に1回, 東北, 関東, 中部, 近畿, 中国, 九州地方整備局では月に2回の更新です.
- 各地方整備局は建設工事やコンサルタント業務など20強の区分について, 入札に参加資格のある事業者の名義, 代表者氏名,　法人所在地, 法人番号, 技術評価点, 財務評価点, 総合評価点を公開しています.   
- 事業は土木, 鋼橋といった建設工事と, 測量や地質調査などのコンサルティング業務があります.

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
    Rootpath = '/Rootpath'

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
3. コマンドラインで以下により, `crawling.py`を実行してください.ここでは, `name`は`kanto`になります
```bash
scrapy crawl name
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
-->
