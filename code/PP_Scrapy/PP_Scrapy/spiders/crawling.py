from urllib import request
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
import jaconv
import re
import sys
import pathlib

class URL_List:

    def __init__(self, index_url, Rootpath):
        self.index_url = index_url
        self.Rootpath = Rootpath

        if index_url.split("/")[-1][-4:] == "html":
            omit_index_html = index_url.split("/")[:-1]
            self.relative_path = '/'.join(omit_index_html)
        elif index_url.split("/")[-1][-3:] == "htm":
            omit_index_html = index_url.split("/")[:-1]
            self.relative_path = '/'.join(omit_index_html)
        else:
            self.relative_path = index_url

    def convert_url_to_soup(self, url):
        html = request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def find_all_arg_of_html_tag(self, url, tag_name, type_name, obj_arg_name):
        """
            指定したhtml tag(tag_name)のうち, 指定したtype(type_name)のもの全てから, 指定した要素(obj_arg_name)を取得する.
        """
        soup = self.convert_url_to_soup(url)
        tag_list = soup.find_all(tag_name, type = type_name)

        obj_list = []
        for i in range(len(tag_list)):
            obj_arg = tag_list[i].get(obj_arg_name)
            obj_list.append(obj_arg)

        return obj_list

    def remove_relative_path(self, path_text):
        # self.relative_pathが/で終わっている場合, "./"を取り除く
        if self.relative_path[-1] == "/":
            path = path_text[path_text.index("/")+1:]
        # self.relative_pathが/で終わっていない場合, "."を取り除く
        else:
            path = path_text[path_text.index("/"):]

        return path

    def find_obj_url(self, ind_url):
        ind_soup = self.convert_url_to_soup(ind_url)
        ind_footnotes = ind_soup.find(attrs={"name": "footnotes"}).get("src")
        obj_url = self.relative_path + self.remove_relative_path(ind_footnotes)
        
        return obj_url

    def find_all_data_url_industry(self, obj_url):
        obj_input_list = self.find_all_arg_of_html_tag(obj_url, "input", "button", "onclick")
        
        data_url_list_each_industry = []
        for i in range(len(obj_input_list)):
            temp = obj_input_list[i].split("'")[1]
            data_path = self.remove_relative_path(temp)
            data_url = self.relative_path + data_path
            data_url_list_each_industry.append(data_url)

        return data_url_list_each_industry

    def find_all_data_url(self):
        path_list = self.find_all_arg_of_html_tag(self.index_url, tag_name = "input", type_name = "radio", obj_arg_name = "value")
        ind_url_list = [self.relative_path + self.remove_relative_path(path) for path in path_list]

        crawling_url_list = []
        for i in range(len(ind_url_list)):
            ind_url = ind_url_list[i]
            obj_url = self.find_obj_url(ind_url)
            data_url_list_each_industry = self.find_all_data_url_industry(obj_url)
            crawling_url_list.extend(data_url_list_each_industry)

        return crawling_url_list

    def convert_JapaneseYear_to_CommonEra(self, warekiYear):

        pattern = re.compile('^(|.+)(明治|大正|昭和|平成|令和)(|\u3000| )([元0-9０-９]+)年(|\u3000| )([0-9０-９]+)月(|\u3000| )([0-9０-９]+)日(|.+)$', re.MULTILINE)
        matches = pattern.search(warekiYear)

        era_name = matches.group(2)
        year = matches.group(4)
        month = jaconv.z2h(matches.group(6), digit = True)
        month = month.zfill(2)
        day = jaconv.z2h(matches.group(8), digit = True)
        day = day.zfill(2)

        if year == '元':
            year = 1
        else:
            if sys.version_info < (3, 0):
                year = year.decode('utf-8')
            year = int(jaconv.z2h(year, digit=True))

        if era_name == '明治':
            year += 1867
        elif era_name == '大正':
            year += 1911
        elif era_name == '昭和':
            year += 1925
        elif era_name == '平成':
            year += 1988
        elif era_name == '令和':
            year += 2018

        return str(year) + month + day

    def get_update_date(self):
        soup = self.convert_url_to_soup(self.index_url)
        date_text = soup.find_all("font")[3].contents[0]
        date = self.convert_JapaneseYear_to_CommonEra(date_text)
        
        return date

    def make_directory(self):
        date_object = self.get_update_date()

        path_construction= pathlib.PosixPath(self.Rootpath + '/construction/' + date_object)
        path_consulting = pathlib.PosixPath(self.Rootpath + '/consulting/' + date_object )

        pathlib.Path.mkdir(path_construction, exist_ok= True, parents=True)
        pathlib.Path.mkdir(path_consulting, exist_ok = True, parents=True)

class Spider(CrawlSpider):
    # set region name
    name = "kanto"

    def __init__(self, category=None, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        # 年度の変更によってindex_url変更の可能性あり.
        self.index_url = 'http://www.ktr.mlit.go.jp/honkyoku/nyuusatu/shikakushinsa/files/'
        self.Rootpath = str(pathlib.Path(__file__).resolve().parents[4]) + "/data/" + self.name + "/qualification"
        print(self.Rootpath)
        self.URL_List = URL_List(self.index_url, self.Rootpath)
        self.start_urls = self.URL_List.find_all_data_url()
        self.date_object = self.URL_List.get_update_date()
        self.URL_List.make_directory()


    def parse(self, response):
        html_name = response.url.split('/')[-1]
        print(html_name)
        print(re.search('\d+', html_name).group())
        if int(re.search('\d+', html_name).group()) < 30:
            filename = self.Rootpath + '/construction/' + self.date_object + '/' + self.name + '_' + self.date_object + '_' + response.url.split("/")[-1]
            print(filename)
        else:
            filename = self.Rootpath + '/consulting/' + self.date_object + '/' + self.name + '_' + self.date_object + '_' + response.url.split("/")[-1]
        
        with open(filename, 'wb') as f:
            f.write(response.body)
