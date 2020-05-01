import pandas as pd
import requests
from html.parser import HTMLParser
import codecs
import bs4
import csv
from lxml import etree
import os
import pathlib
import re

colname = [['firm_name', 'firm_id', 'prefecture', 'firm_size'],
           ['surveying_rank', 'surveying_exception'], 
           ['buildingConsulting_rank', 'buildingConsulting_exception'], 
           ['civilEngineeringConsulting_rank', 'civilEngineeringConsulting_exception'], 
           ['geologicalSurvey_rank', 'geologicalSurvey_exception'],
           ['compensationConsultanting_rank', 'compensationConsultanting_exception'],
           ['date']]

def clean_html(filename):
    html = open(filename,  encoding="cp932").read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    [tag.extract() for tag in soup(string='\n')]
    table = soup.find("div")
    firm_list = table.find_all("tr")
    
    df = pd.DataFrame(columns = sum(colname, []))
    for i in range(0, len(firm_list) , 2):
        firm = pd.Series(index = sum(colname, []))
        firm_qualifiation = firm_list[i].find_all('td')
        firm_data = [content.text for content in firm_list[i+1].find_all("p")]
        # exception : joint venture flag
        if (not re.search( '（共）', firm_qualifiation[0].a.text) == None) and (len(firm_data[0]) == 0):
            firm_data[0] = 'JV'
        
        firm['firm_name'] = firm_qualifiation[0].a.text
        firm['firm_id', 'prefecture', 'firm_size'] = firm_data
        firm['date'] = filename.split("/")[-2]
    
        for i in range(1, len(firm_qualifiation)):
            firm_ind = list(firm_qualifiation[i].p.find("font").strings)
            
            if len(firm_ind) == 0:
                firm[colname[i]] = ['', '']
            elif (len(firm_ind) == 1) and (firm_ind[0] in ['\u3000', ' ']):
                firm[colname[i]] = ['', '']
            elif len(firm_ind) == 1:
                firm[colname[i]] = [firm_ind[0], '']
            else:
                firm[colname[i]] = firm_ind

        df = df.append(firm, ignore_index = True)
    print(df)
    return df


def list_all_files(directory, extension=None, size=None, sort=False):
    if extension is not None and extension[0] != ".":
        extension = "." + extension

    directory = pathlib.Path(directory)

    path_list = []
    files = directory.glob("**/*")

    if size is None:
        for file in files:
            if file.is_file() and (extension is None or file.suffix == extension):
                path_list.append(str(file))
    else:
        for i, obj in enumerate(files):
            if len(path_list) >= size:
                break
            
            if file.is_file() and (extension is None or file.suffix == extension):
                path_list.append(str(file))

    if sort:
        path_list.sort()

    return path_list
    
def make_panel(file_list):
    if file_list == None:
        print("ValueError : file_list is None")

    else:
        panel_df = pd.DataFrame(columns= sum(colname, []))
        for file in file_list:
            df = clean_html(file)
            panel_df = panel_df.append(df, ignore_index=True)
            panel_df = panel_df[~panel_df[['firm_name', 'date']].duplicated()]
           
            
        return panel_df
    
def make_csv(file_list, directory):
    panel_df = make_panel(file_list)
    panel_df.to_csv(directory, encoding='utf_8_sig')


def get_input_directory(region, date):
    path = pathlib.Path(__file__).resolve()
    directory = str(path.parent.parent) + "/data/" + region + "/qualification/consulting/" + date

    return directory


def set_output_directory(region, date):
    path = pathlib.Path(__file__).resolve()
    # make output directory
    path_dir = pathlib.Path(str(path.parent.parent) + "/data/" + region)
    pathlib.Path.mkdir(path_dir, exist_ok = True, parents=True)
    # file name
    directory = str(path.parent.parent) + "/data/" + region + "/qualification/" + region + "_consulting_" + date + ".csv"
    
    return directory

 
if __name__ == "__main__":

    region = 'kanto'
    # dataが存在する日付を指定
    dates = ["20200501"]


    for date in dates:
      output_directory = set_output_directory(region, date)
      file_list = list_all_files(get_input_directory(region, date), extension= 'html', sort = True)
      make_csv(file_list, output_directory)




